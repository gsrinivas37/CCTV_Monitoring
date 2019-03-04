#!/usr/bin/python
import os.path
import os
import datetime
import shutil
import cv2

def get_files(parent_dir, extension):
    return [x for x in os.listdir(parent_dir) if x.endswith(extension)]
    
def get_sub_dirs(root_dir):
    return [x for x in os.listdir(root_dir) if os.path.isdir(root_dir+"/"+x)]

def ensure_dir_exists(directory):
	if not os.path.exists(directory):
		os.mkdir(directory)

def replace_with_low_res(directory, files):
    print("Running replace_with_low_res on :"+directory)
    for img in files:
        try:
            cv2_img = cv2.imread(os.path.join(directory,img))
            if str(cv2_img.shape) == "(360, 640, 3)":
                continue
            cv2_img = cv2.resize(cv2_img, (640, 360))
            cv2.imwrite(os.path.join(os.path.join(directory,"temp.jpg")), cv2_img)
            os.remove(os.path.join(directory,img))
            os.rename(os.path.join(os.path.join(directory,"temp.jpg")), os.path.join(directory,img))
        except:
            print("error reading:"+img)

def save_space(date_dir):
    print("Running save_space on date:"+date_dir)
    for hour_dir in get_sub_dirs(date_dir):
        all_images = get_files(os.path.join(date_dir, hour_dir), "jpg")
        non_person_imgs = all_images
        person_dir = os.path.join(date_dir,hour_dir,"persons")
        if os.path.exists(person_dir):
            person_imgs = get_files(person_dir,"jpg")
            non_person_imgs = [x for x in all_images if x not in person_imgs]

        replace_with_low_res(os.path.join(date_dir,hour_dir),non_person_imgs)

def save_space_video(date_dir):
    print("Running save_space_video on date:"+date_dir)
    for hour_dir in get_sub_dirs(date_dir):
        person_dir = os.path.join(date_dir,hour_dir,"persons")
        if not os.path.exists(person_dir):
            print("Person dir doesn't exist on "+hour_dir)
            gate_video = os.path.join(date_dir.replace("Photos","Videos"),hour_dir)
            print("Remove directory:"+gate_video)
            if os.path.exists(gate_video):
                shutil.rmtree(gate_video)