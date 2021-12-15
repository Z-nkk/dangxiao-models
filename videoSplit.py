#!/usr/bin/python
# -*- coding: utf-8 -*-
#import pdb
import json
import datetime
import myrabbitmq
#import numpy as np
import time
# RabbitMq服务器相关
import cv2
from multiprocessing import Process
#minioclient = MinioClass()


def Video2Img(task):
    print('start print task:')
    print(task)  
    Cap = dict()
    Images = dict()
    #pdb.set_trace()
    starttime = datetime.datetime.strptime(task['time'], "%Y-%m-%d %H:%M:%S")
    ValidArea = dict()
    FrontArea = dict()
    CenterArea = dict()
    if task['taskType'] == 'VIDEO':
        CameraList = task['cameraConfig']
        #inter = [0, 0, 0, 0, 1, 0, 1, 0, 0]
        #task['samplingPeriod'] = 5
        #task['samplingNum'] = 9
        for camera in CameraList:
            rtsp = camera['video']
            Cap[camera['cameraId']] = cv2.VideoCapture(rtsp)
            fps = Cap[camera['cameraId']].get(cv2.CAP_PROP_FPS)#算相机的帧速率FPS.
            total = Cap[camera['cameraId']].get(cv2.CAP_PROP_FRAME_COUNT)## 视频文件的帧数
            print(fps)
            print(total)
            
            if task['areaCountFlag']:
                temparea = []
                for point in camera['validArea']:
                    temparea.append([point['x'],point['y']])
                #temparea = np.array(temparea)
                ValidArea[camera['cameraId']] = temparea
                temparea = []
                for point in camera['frontArea']:
                    temparea.append([point['x'],point['y']])
                #temparea = np.array(temparea)
                FrontArea[camera['cameraId']] = temparea
                temparea = []
                for point in camera['centerArea']:
                    temparea.append([point['x'],point['y']])

                CenterArea[camera['cameraId']] = temparea


        print('Cap=',Cap)
        for i in range(int(task['samplingNum'])):
            index = int(fps*task['samplingPeriod']*i) 
            print('index=',index)
            Time = (starttime + datetime.timedelta(seconds=task['samplingPeriod']*i)).strftime("%Y%m%d%H%M%S")
            Time_standard = (starttime + datetime.timedelta(seconds=task['samplingPeriod']*i)).strftime("%Y-%m-%d %H:%M:%S")
            for camera in CameraList:
                Cap[camera['cameraId']].set(cv2.CAP_PROP_POS_FRAMES,index)
                ret,Images[camera['cameraId']] = Cap[camera['cameraId']].read()
 
            NewCameraList = []
            NewImages = dict()
            for camera in CameraList:
                path = '/data/SmartEducationImage/source/'+Time + '_' + camera['cameraId'] +'.jpg'
                cv2.imwrite(path,Images[camera['cameraId']])
                NewCameraList.append(camera['cameraId'])
                NewImages[camera['cameraId']] = path

            
            
            subtask = dict()
            #subtask['taskId'] = task['taskIdList'][i]
            subtask['cameraNum'] = task['cameraNum']
            subtask['camerasConfig'] = task['cameraConfig']
            subtask['taskType'] = task['taskType']
            subtask['lessonId'] = task['lessonId']
            subtask['CameraList'] = NewCameraList
            subtask['Images'] = NewImages
            #subtask['MinioImages'] = MinioImages
            subtask['ValidArea'] = ValidArea
            subtask['FrontArea'] = FrontArea
            subtask['CenterArea'] = CenterArea
            subtask['Time'] = Time
            subtask['TimeS'] = Time_standard
            #subtask['inter'] = inter[i]
            if i == int(task['samplingNum']) - 1:
                subtask['is_last'] = True
            else:
                subtask['is_last'] = False
            subtask = json.dumps(subtask,indent=2)

            print('subtask=',subtask)
            myrabbitmq.RabbitPublisher.run('testAction1', str(subtask), 'testExchange', 'subtaskQueue')
    elif task['taskType'] == 'REALTIME':
        CameraList = task['cameraConfig']
        #task['samplingPeriod'] = 5
        if task['areaCountFlag']:
            for camera in CameraList:
                temparea = []
                for point in camera['validArea']:
                    temparea.append([point['x'],point['y']])
                ValidArea[camera['cameraId']] = temparea
                temparea = []
                for point in camera['frontArea']:
                    temparea.append([point['x'],point['y']])
                FrontArea[camera['cameraId']] = temparea
                temparea = []
                for point in camera['centerArea']:
                    temparea.append([point['x'],point['y']])
                CenterArea[camera['cameraId']] = temparea

        for i in range(int(task['samplingNum'])):
            
            
            Time = (starttime + datetime.timedelta(seconds=task['samplingPeriod']*i)).strftime("%Y%m%d%H%M%S")
            Time_standard = (starttime + datetime.timedelta(seconds=task['samplingPeriod']*i)).strftime("%Y-%m-%d %H:%M:%S")


            
            for camera in CameraList:
                rtsp = camera['rtsp']
                while True:
                    Cap[camera['cameraId']] = cv2.VideoCapture(rtsp)
                    ret, Images[camera['cameraId']] = Cap[camera['cameraId']].read()
                    if ret:
                        if Images[camera['cameraId']] is None:
                            Cap[camera['cameraId']].release()
                        else:
                            Cap[camera['cameraId']].release()
                            break
                    else:
                        Cap[camera['cameraId']].release()


            NewCameraList = []
            NewImages = dict()
            #Images = dict()
            for camera in CameraList:
                path = '/data/SmartEducationImage/source/'+Time + '_' + camera['cameraId'] +'.jpg'
                cv2.imwrite(path,Images[camera['cameraId']])
                NewCameraList.append(camera['cameraId'])
                NewImages[camera['cameraId']] = path
              
            
            subtask = dict()
            #subtask['taskId'] = task['taskIdList'][i]
            subtask['taskType'] = task['taskType']
            subtask['lessonId'] = task['lessonId']
            subtask['camerasConfig']=task['cameraConfig']
            subtask['CameraList'] = NewCameraList
            subtask['Images'] = NewImages
            #subtask['MinioImages'] = MinioImages
            subtask['ValidArea'] = ValidArea
            subtask['FrontArea'] = FrontArea
            subtask['CenterArea'] = CenterArea
            subtask['Time'] = Time
            subtask['TimeS'] = Time_standard
            if i == int(task['samplingNum']) - 1:
                subtask['is_last'] = True
            else:
                subtask['is_last'] = False
            subtask = json.dumps(subtask,indent=2)

            print(subtask)
            myrabbitmq.RabbitPublisher.run('testAction1', str(subtask), 'testExchange', 'subtaskQueue')
            
            time.sleep(task['samplingPeriod']) 
    print('task is done')
    
   
def consumer_callback(ch, method, properties, body):
    #process_id = threading.current_thread()
    ch.basic_ack(delivery_tag=method.delivery_tag)
    # time.sleep(5)
    print(body)
    body = body.decode('utf-8')
    #print("当前的进程id为：%s ，接收到消息： %s 。" % (process_id, body))
    print(type(body))
    body = json.loads(body)
    #print(body)
    #print(type(body))

    p = Process(target=Video2Img,args=(body,))
    p.start()

# 主函数
if __name__ == '__main__':
    
    queue = 'dev-VideoCapture'
    exchange = 'dev-VideoCaptureExchange'

    myrabbitmq.RabbitConsumerVideo.run(consumer_callback,exchange,queue)
