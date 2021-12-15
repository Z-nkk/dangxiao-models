#-*- coding: utf-8 -*-
import math
def get_angle(keypoint, x, y, z):
        angle = -1
        if keypoint[x,0] > 0 and keypoint[y,0] > 0 and keypoint[z,0] > 0:
            a = math.pow(keypoint[x,1]-keypoint[y,1],2) + math.pow(keypoint[x,0]-keypoint[y,0],2)
            b = math.pow(keypoint[z,1]-keypoint[y,1],2) + math.pow(keypoint[z,0]-keypoint[y,0],2)
            c = math.pow(keypoint[z,1]-keypoint[x,1],2) + math.pow(keypoint[z,0]-keypoint[x,0],2)
            if a > 0 and b > 0 and c > 0 and (a+b-c)/(2*math.sqrt(a*b)) >= -1 and (a+b-c)/(2*math.sqrt(a*b)) <= 1:
                angle = math.acos((a+b-c)/(2*math.sqrt(a*b)))
                angle = angle*180/math.pi
            #print(angle)
        return int(angle)

'''
Input:
    poseKeypoint: skeleton output by OpenPose
Output:
    0:other   1:headUp  2:headDown
'''
def HeadMetric(poseKeypoint):
    if poseKeypoint.ndim < 2:
        return 0
    else:

        angle = get_angle(poseKeypoint, 0, 1, 8)
        if angle > 120:
            return 1
        elif angle < 40:
            return 2
        else:
            return 0
