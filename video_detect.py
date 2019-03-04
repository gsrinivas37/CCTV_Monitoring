import time
from shared import *
from detector import DetectorAPI

def get_videos(date,hour):
    videos = []
    for video_root in video_root_dirs:
        for file in get_files(os.path.join(video_root,date,hour),"mp4"):
            videos.append(os.path.join(video_root,date,hour,file))
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
                currentframe +=1
                continue
            boxes, scores, classes, num = odapi.processFrame(frame)
            for i in range(len(boxes)):
                # Class 1 represents human
                if classes[i] == 1 and scores[i] > threshold:
                    cam.release()
                    return True
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
        print("Person exists in "+ vid)
    else:
        print("No person exists in "+ vid)
        f = open(vid+".noperson","w")
        f.write("No Person")
        f.close()

total_time = time.time() - start_time
str = ("Video detect ran at %s on %d videos and took %d minutes and %d seconds\n")%(now.strftime("%Y-%m-%d %H:%M"),len(all_videos),total_time/60, total_time%60)
print(str)
