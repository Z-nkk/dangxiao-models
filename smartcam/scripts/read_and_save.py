"""
read a camera and save captured frames
"""

import cv2
import argparse
from pathlib import Path
import os
from datetime import datetime


parser = argparse.ArgumentParser()
# parser.add_argument("cam_ip_path", help="path/to/cam_ip.csv")
parser.add_argument("rtsp_format_path", help="path/to/rtsp_format.txt")
parser.add_argument("out_dir", help="path/to/output_dir")
args = parser.parse_args()

Path(args.out_dir).mkdir(parents=True, exist_ok=True)

# ======== configurations ======
loc = "b-1f"
cam_ip = "192.168.12.61"
total_n = 300
freq = 30
# ==============================

with open(args.rtsp_format_path, "r") as fin:
    username = fin.readline().strip()
    password = fin.readline().strip()
    url = fin.readline().strip()


rtsp_url = f"rtsp://{username}:{password}@{cam_ip}{url}"
cam = cv2.VideoCapture(rtsp_url)
for idx in range(total_n):
    ret, f = cam.read()
    if ret:
        if idx % freq == 0:
            t = datetime.now().strftime('%Y%m%d%H%M%S')
            out_filename = f"{loc}_{cam_ip}_{t}.jpg"
            out_path = os.path.join(args.out_dir, out_filename)
            cv2.imwrite(out_path, f)
            print(f"{out_path} saved.")
    else:
        print(f"cannot open camera: {loc} -- {cam_ip}")
cam.release()