# Code adapted from Tensorflow Object Detection Framework
# https://github.com/tensorflow/models/blob/master/research/object_detection/object_detection_tutorial.ipynb
# Tensorflow Object Detection Detector

import time
import datetime
from shared import *
from detector import DetectorAPI

def get_videos(date,hour):
    videos = []
    gate_root = '/mnt/hdd/GateVideos'
    stairs_root = '/mnt/hdd/StairsVideos'
    for file in get_files(os.path.join(gate_root,date,hour),"mp4"):
        videos.append(os.path.join(gate_root,date,hour,file))

    for file in get_files(os.path.join(stairs_root,date,hour),"mp4"):
        videos.append(os.path.join(stairs_root,date,hour,file))

    return videos

def person_exists_in_video(video):
    print("Video detect on.. " + video)

    # Read the video from specified path
    cam = cv2.VideoCapture(video)

    # frame
    currentframe = 0

    while (True):
        # reading from frame
        ret, frame = cam.read()

        if ret:
            if currentframe % 50 != 0:
                continue

            # if video is still left continue creating images
            # print('Process frame No.' + str(currentframe))

            boxes, scores, classes, num = odapi.processFrame(frame)

            for i in range(len(boxes)):
                # Class 1 represents human
                if classes[i] == 1 and scores[i] > threshold:
                    cam.release()
                    return True

            # increasing counter so that it will
            # show how many frames are created
            currentframe += 1
        else:
            break

    # Release all space and windows once done
    cam.release()
    return False

start_time = time.time()
now = datetime.datetime.now()
lasthour = now - datetime.timedelta(hours=1)
date = lasthour.strftime("%Y-%m-%d")

model_path = '/home/pi/tensorflow1/models/research/object_detection/ssdlite_mobilenet_v2_coco_2018_05_09/frozen_inference_graph.pb'
odapi = DetectorAPI(path_to_ckpt=model_path)
threshold = 0.5

hour = '%02dhour'%(lasthour.hour)
all_videos = get_videos(date,hour)
print("No. of videos to process: "+str(len(all_videos)))

for vid in all_videos:
    if person_exists_in_video(vid)==True:
        print("Peron exists in "+ vid)
    else:
        f = open(vid+".noperson")
        f.write("No Person")
        f.close()

total_time = time.time() - start_time
str = ("Video detect ran at %s on %d videos and took %d minutes and %d seconds\n")%(now.strftime("%Y-%m-%d %H:%M"),len(all_videos),total_time/60, total_time%60)
print(str)
