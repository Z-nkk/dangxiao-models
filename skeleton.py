#-*- coding: utf-8 -*-

# From Python
# It requires OpenCV installed for Python
import sys
import cv2
import os
from sys import platform
import numpy as np
import yaml
import time
import datetime
#import pynvml
sys.path.append('/data/workspace/openpose/build/python/openpose')
import pyopenpose as op

class OpenPose:
    def __init__(self, cnf_file=""):
        #y = yaml.load(open(cnf_file,'r'))#读取yaml配置文件.python通过open方式读取文件数据，再通过load函数将数据转化为列表或字典；
        # Custom Params (refer to include/openpose/flags.hpp for more parameters)
        
        #os.environ["CUDA_VISIBLE_DEVICES"] = y['use_gpu']#获取有关系统的各种信息,os.environ 是一个字典，是环境变量的字典
        params = dict()
        #params["model_folder"] = y['model_folder']
        params["model_folder"] = '/data/workspace/openpose/models'
        #params["net_resolution"] = y['resolution']
        #params["net_resolution"]='2048x1088'
        #params["net_resolution"]='1920x960'
        #params["net_resolution"]='1120x640'
        #params["net_resolution"]='960x480'
        #params["net_resolution"]='800x320'

        # Starting OpenPose
        print("OpenPose 启动中 ...")

        time_start = time.time()

        self.opWrapper = op.WrapperPython()
        self.opWrapper.configure(params)
        self.opWrapper.start()
        time_end = time.time()

        print('OpenPose 启动完成，耗时：',time_end - time_start,'秒.')
        
   
    def infer(self, image):
        #print(image.shape)
        # Process Image
        try:
            datum = op.Datum() #线程之间的基本信息
            datum.cvInputData = image
            #datum.poseKeypoints = [[1]]
            #datum.poseKeypoints = np.array([[[1.4, 3.5, 0.5]]],dtype=np.float32)
            self.opWrapper.emplaceAndPop(op.VectorDatum([datum]))
        except Exception as e:
            print( datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            print(e)
        return datum
    
    def dump(self, datum,img_name):
        print("Body keypoints: \n" + str(datum.poseKeypoints.shape[0]))
        #for i in range(datum.poseKeypoints.shape[0]):
        #    xx = datum.poseKeypoints[i][:,0]
        #    xx = xx[xx!=0]
        #    yy = datum.poseKeypoints[i][:,1]
        #    yy = yy[yy!=0]
        #    cv2.rectangle(img,(int(min(xx)),int(max(yy))),(int(max(xx)),int(min(yy))),(255,255,0),2)#rectangle在任何图像上绘制矩形
        cv2.imwrite(img_name,datum.cvOutputData)
        #cv2.imwrite('output7.png',img)
 
if __name__ == "__main__":
    
    os.environ["CUDA_VISIBLE_DEVICES"] = '0'
    opper = OpenPose()
    while(1):
        for i in range(3,4):
            img = cv2.imread('frames11/frame2925-7-'+str(i)+'.png')
            print("OpenPose 测试 ...")
            time_start = time.time()
            result = opper.infer(img)
            #print(result.poseKeypoints)
            time_end = time.time()
            print('OpenPose 测试完成，耗时：',time_end - time_start,'秒.')
            opper.dump(result, img,'output2925-7-'+str(i)+'.png')
    
        
    


