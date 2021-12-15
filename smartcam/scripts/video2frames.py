"""
read a video and save frames as .jpg files
"""

import cv2
import argparse
from pathlib import Path
import os

parser = argparse.ArgumentParser()
parser.add_argument("video_path", help="/path/to/video.mp4")
parser.add_argument("out_dir", help="path/to/output_dir")
parser.add_argument("freq", help="save one frame per [freq]", default=1, type=int)
args = parser.parse_args()

Path(args.out_dir).mkdir(parents=True, exist_ok=True)

vid = cv2.VideoCapture(args.video_path)
idx = 0
video_name = args.video_path.split('/')[-1][:-4]

while True:
    ret, f  = vid.read()
    if not ret:
        break
    idx += 1
    if idx % args.freq == 0:
        out_path = os.path.join(args.out_dir, f"{video_name}_{idx}.jpg")
        cv2.imwrite(out_path, f)
    if idx % 100 == 0:
        print(f"{idx} frames processed.")
vid.release()