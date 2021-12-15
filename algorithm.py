import json
import cv2
import numpy as np
import skeleton
import myrabbitmq
import sys 
import seatMatch
import recognition
from minioclass import MinioClass

sys.path.append('./smartcam')
from linkeaction import SinglePersonSVM

minioclient = MinioClass()
opper = skeleton.OpenPose()
model = SinglePersonSVM(weights_path="./smartcam/weights/pose_svm_dangxiao_v1.pkl")

#behavmap={1:'sleep',2:'handUp',3:'headDown'}
#seatmap={'seat1':'student1','seat2':'student2','seat3':'student3'}

idx2act = ["", "sleep", "raiseHand", "takeNote", "usePhone", "headUp"]
samplingOrder=1

def mycallback(ch, method, properties, body):
    global samplingOrder
    ch.basic_ack(delivery_tag=method.delivery_tag)
    body = body.decode('utf-8')
    print("mycallback body:")
    print(body)
    task = json.loads(body)
    print("mycallback task:")
    print(task)

    seatCfg = dict()
    for cameraCfg in task['camerasConfig']:
        seatCfg[cameraCfg['cameraId']]=cameraCfg['seatConfig']

    for camera in task['CameraList']:
        sleep=0
        handUp=0
        takeNote=0
        usePhone=0
        
        headUp=0
        headDown=0

        #behav_rs = dict()
        output = dict()

        datum = opper.infer(cv2.imread(task['Images'][camera]))
        print(datum.poseKeypoints.shape)
        skeleton_img='/data/SmartEducationImage/skeleton/'+task['Time']+'_'+camera+'.jpg'
        opper.dump(datum,skeleton_img)
        #output['sourceImg']=skeleton_img
        #output['sourceImg']=task['Images'][camera]
        
        miniopath_source='image/source/'+task['Time'] + '_' + camera +'.jpg'
        minioclient.upload(miniopath_source,task['Images'][camera])
        output['sourceImg'] = 'education/'+miniopath_source
        
        miniopath_skeleton='image/skeleton/'+task['Time'] + '_' + camera +'.jpg'
        minioclient.upload(miniopath_skeleton,skeleton_img)
        output['skeletonImg'] = 'education/'+miniopath_skeleton
        
        output['faceImg'] = ''
       
        ##save
        #np.save('pose',datum.poseKeypoints)
        ##seat match
        ssdict = dict()
        if seatCfg.__contains__(camera):
            tmpdic=dict()
            tmpdic['seatConfig'] = seatCfg[camera]
            seatCfgJson = json.dumps(tmpdic)
            print(seatCfgJson)
            ssM = seatMatch.ssMatch(seatCfgJson,datum.poseKeypoints)
            ssdict,absent = ssM.match()
            print(ssdict)

        behavList = []
        index=0
        ##behavior
        for kp in datum.poseKeypoints:
            # pose: 25x3
            #label = idx2act[model.predict(kp)]
            
            behav = model.predict(kp.reshape(75))
            headUpDown=recognition.HeadMetric(kp)
            if headUpDown == 1 and behav ==4:
                behav = 5

            if ssdict.__contains__(index):
                studentBehav = dict()
                studentBehav['studentId'] = ssdict[index]
                studentBehav['behavior']= idx2act[behav]
                behavList.append(studentBehav)
                index += 1
            else:
                index += 1
                continue
            
            #for student in absent:
            #    studentAbsent = dict()
            #    studentAbsent['studentId'] = student
            #    studentAbsent['behavior']= 'absent'
            #    behavList.append(studentAbsent)

            if behav == 1:
                sleep += 1
            elif behav == 2:
                handUp += 1
            elif behav == 3:
                takeNote += 1
            elif behav == 4:
                usePhone += 1
            elif behav == 5:
                headUp += 1
            else:
                pass


        output['taskType'] = task['taskType']
        output['lessonId'] = task['lessonId']
        output['cameraNum'] = task['cameraNum']
        output['cameraId'] = camera
        output['time'] = task['TimeS'] 
        output['samplingOrder'] = samplingOrder
        if task['is_last'] == True:
            output['status'] = "finished"
        else:
            output['status'] = "continue"

        result = dict()
        result['present']=sleep+handUp+takeNote+usePhone+headUp
        result['absent']=len(absent)
        result['sleep']=sleep
        result['takeNote'] = takeNote
        result['usePhone'] = usePhone
        result['raiseHand']=handUp
        result['headUp']=headUp
        #result['headDown']=headDown

        output['result']=result

        for student in absent:
            studentAbsent = dict()
            studentAbsent['studentId'] = student
            studentAbsent['behavior']= 'absent'
            behavList.append(studentAbsent)

        output['behaviorInfo'] = behavList
        output_json = json.dumps(output)
        print(result)
        #myrabbitmq.RabbitPublisher.run('testAction1', str(output_json), 'ResultSaverExchange', 'ResultSaver')
        #myrabbitmq.RabbitPublisher.run('testAction1', str(output_json), 'pengEx', 'pengQueue')
        myrabbitmq.RabbitPublisher.run('testAction1', str(output_json), '', 'ResultSaver')
        
    samplingOrder = samplingOrder + 1
    if task['is_last'] == True:
        samplingOrder=1

if __name__ == '__main__':

    queue = 'subtaskQueue'
    exchange = 'testExchange'

    myrabbitmq.RabbitConsumerVideo.run(mycallback,exchange, queue)
