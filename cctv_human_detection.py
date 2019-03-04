# Code adapted from Tensorflow Object Detection Framework
# https://github.com/tensorflow/models/blob/master/research/object_detection/object_detection_tutorial.ipynb
# Tensorflow Object Detection Detector

import cv2
import time
import os
import os.path
import datetime
from shared import *
from detector import DetectorAPI

def runOnDirectory(root_dir,date,hour):
    cur_dir = os.path.join(root_dir,date,hour)
    tar_dir = os.path.join(root_dir,date,hour,"persons")

    print("Running on.. "+cur_dir)
    images = get_files(cur_dir, "jpg")
    for x in images:
        #print(x)
        
        try:
            img = cv2.imread(cur_dir+"/"+x)
            img = cv2.resize(img, (1280, 720))
        except Exception as e:
            print("Error reading file:"+x)
            continue

        boxes, scores, classes, num = odapi.processFrame(img)

        # Visualization of the results of a detection.

        for i in range(len(boxes)):
            # Class 1 represents human
            if classes[i] == 1 and scores[i] > threshold:
                if not os.path.exists(tar_dir):
                    os.mkdir(tar_dir)
                thumbnail = os.path.join(cur_dir,"thumbnails",x)
                if os.path.exists(thumbnail):
                    os.symlink(thumbnail,tar_dir+"/"+x)
                else:
                    img = cv2.resize(img, (400, 225))
                    cv2.imwrite(tar_dir+"/"+x, img)
                break
                #box = boxes[i]
                #cv2.rectangle(img,(box[1],box[0]),(box[3],box[2]),(255,0,0),2)

        #cv2.imwrite("/home/pi/face/out/"+x, img)
    return len(images)

start_time = time.time()
now = datetime.datetime.now()
lasthour = now-datetime.timedelta(hours=1)
date = lasthour.strftime("%Y-%m-%d")
    
model_path = '/home/pi/tensorflow1/models/research/object_detection/ssdlite_mobilenet_v2_coco_2018_05_09/frozen_inference_graph.pb'
odapi = DetectorAPI(path_to_ckpt=model_path)
threshold = 0.5
    
hour = '%02dhour'%(lasthour.hour)

total = 0
for photo_root in photo_root_dirs:
    total = total + runOnDirectory(photo_root,date,hour)

total_time = time.time() - start_time
str = ("Person detect ran at %s on %d images and took %d minutes and %d seconds\n")%(now.strftime("%Y-%m-%d %H:%M"),total,total_time/60, total_time%60)
print(str)