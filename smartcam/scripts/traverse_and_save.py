"""
traverse a camera list and save captured frames
"""

import cv2
import argparse
from pathlib import Path
import os
from datetime import datetime


parser = argparse.ArgumentParser()
parser.add_argument("cam_ip_path", help="path/to/cam_ip.csv")
parser.add_argument("rtsp_format_path", help="path/to/rtsp_format.txt")
parser.add_argument("out_dir", help="path/to/output_dir")
args = parser.parse_args()

Path(args.out_dir).mkdir(parents=True, exist_ok=True)

loc_list = []
cam_ip_list = []
with open(args.cam_ip_path, "r") as fin:
    heads = fin.readline()
    for line in fin.readlines():
        tmp = line.strip().split(",")
        loc = tmp[0]
        cam_ip = tmp[1]
        loc_list.append(loc)
        cam_ip_list.append(cam_ip)
    print(f"{len(cam_ip_list)} cameras.")

with open(args.rtsp_format_path, "r") as fin:
    username = fin.readline().strip()
    password = fin.readline().strip()
    url = fin.readline().strip()

for loc, cam_ip in zip(loc_list, cam_ip_list):
    rtsp_url = f"rtsp://{username}:{password}@{cam_ip}{url}"
    cam = cv2.VideoCapture(rtsp_url)
    ret, f = cam.read()
    if ret:
        t = datetime.now().strftime('%Y%m%d%H%M%S')
        out_filename = f"{loc}_{cam_ip}_{t}.jpg"
        out_path = os.path.join(args.out_dir, out_filename)
        cv2.imwrite(out_path, f)
        print(f"{out_path} saved.")
    else:
        print(f"cannot open camera: {loc} -- {cam_ip}")
    cam.release()