# Code adapted from Tensorflow Object Detection Framework
# https://github.com/tensorflow/models/blob/master/research/object_detection/object_detection_tutorial.ipynb
# Tensorflow Object Detection Detector

import numpy as np
import tensorflow as tf
import cv2
import time
import os
import os.path
import datetime
import sys

class DetectorAPI:
    def __init__(self, path_to_ckpt):
        self.path_to_ckpt = path_to_ckpt

        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(self.path_to_ckpt, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

        self.default_graph = self.detection_graph.as_default()
        self.sess = tf.Session(graph=self.detection_graph)

        # Definite input and output Tensors for detection_graph
        self.image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
        # Each box represents a part of the image where a particular object was detected.
        self.detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
        # Each score represent how level of confidence for each of the objects.
        # Score is shown on the result image, together with the class label.
        self.detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
        self.detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
        self.num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')

    def processFrame(self, image):
        # Expand dimensions since the trained_model expects images to have shape: [1, None, None, 3]
        image_np_expanded = np.expand_dims(image, axis=0)
        # Actual detection.
        #start_time = time.time()
        (boxes, scores, classes, num) = self.sess.run(
            [self.detection_boxes, self.detection_scores, self.detection_classes, self.num_detections],
            feed_dict={self.image_tensor: image_np_expanded})
        #end_time = time.time()

        #print("Elapsed Time:", end_time-start_time)

        im_height, im_width,_ = image.shape
        boxes_list = [None for i in range(boxes.shape[1])]
        for i in range(boxes.shape[1]):
            boxes_list[i] = (int(boxes[0,i,0] * im_height),
                        int(boxes[0,i,1]*im_width),
                        int(boxes[0,i,2] * im_height),
                        int(boxes[0,i,3]*im_width))

        return boxes_list, scores[0].tolist(), [int(x) for x in classes[0].tolist()], int(num[0])

    def close(self):
        self.sess.close()
        self.default_graph.close()

def get_files(parent_dir, extension):
    return [x for x in os.listdir(parent_dir) if x.endswith(extension)]

def runOnDirectory(root_dir,date,hour):
    #print("Running on.. "+root_dir)
    cur_dir = os.path.join(root_dir,date,hour)
    tar_dir = os.path.join(root_dir,date,hour,"persons")

    images = get_files(cur_dir, "jpg")
    for x in images:
        #print(x)
        
        img = cv2.imread(cur_dir+"/"+x)
        img = cv2.resize(img, (1280, 720))

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
                    img = cv2.resize(img, (288, 162))
                    cv2.imwrite(tar_dir+"/"+x, img)
                break
                #box = boxes[i]
                #cv2.rectangle(img,(box[1],box[0]),(box[3],box[2]),(255,0,0),2)

        #cv2.imwrite("/home/pi/face/out/"+x, img)
    return len(images)

if __name__ == "__main__":
    start_time = time.time()
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    
    if now.hour==0:
        sys.exit(0)
    
    model_path = '/home/pi/tensorflow1/models/research/object_detection/ssdlite_mobilenet_v2_coco_2018_05_09/frozen_inference_graph.pb'
    odapi = DetectorAPI(path_to_ckpt=model_path)
    threshold = 0.4
    
    hour = '%02dhour'%(now.hour-1)
        
    total = runOnDirectory("/mnt/hdd/GatePhotos",date,hour)
    total = total + runOnDirectory("/mnt/hdd/StairsPhotos",date,hour)
    
    total_time = time.time() - start_time
    log_file = "/home/pi/www/logs/person_detect/log.txt"
    str = ("Person detect ran at %s on %d images and took %d minutes and %d seconds\n")%(now.strftime("%Y-%m-%d %H:%M"),total,total_time/60, total_time%60)
    f = open(log_file, "a")
    f.write(str)
    f.close()
    
    
    #print("Overall Time:", end_time-start_time)
