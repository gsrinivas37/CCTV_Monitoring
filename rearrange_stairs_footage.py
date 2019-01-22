#!/usr/bin/python
import os.path
import os
import datetime
import glob
import shutil
import cv2

stairs_root_dir = "/mnt/hdd/tmp/StairsCamera/"
stairs_target_imgs_dir = "/mnt/hdd/StairsPhotos/"
stairs_target_vids_dir = "/mnt/hdd/StairsVideos/"


def get_sub_dirs(root_dir):
    return [x for x in os.listdir(root_dir) if os.path.isdir(root_dir+"/"+x)]
    
def ensure_dir_exists(directory):
	if not os.path.exists(directory):
		os.mkdir(directory)

def get_hour(img):
	return img.split('/')[8]+"hour"

def get_min(img):
	return img.split('/')[9]
	
def move_images(dt):
	imgs = []
	for img in  glob.iglob(dt_path+'/**/*.jpg', recursive=True):
		imgs.append(img)
	
	print("No. of images to be moved are :"+str(len(imgs)))
	if len(imgs)!=0:
		ensure_dir_exists(stairs_target_imgs_dir+dt)
		for img in imgs:
			hr = get_hour(img)
			ensure_dir_exists(stairs_target_imgs_dir+dt+"/"+hr)
			thumbnail_dir = os.path.join(stairs_target_imgs_dir+dt,hr,"thumbnails")
			ensure_dir_exists(thumbnail_dir)
			dest_path = os.path.join(stairs_target_imgs_dir+dt,hr,hr[:2]+"_"+get_min(img)+"_"+os.path.split(img)[1])
			shutil.move(img,dest_path)
			
			cv2_img = cv2.imread(dest_path)
			cv2_img = cv2.resize(cv2_img, (320, 180))
			cv2.imwrite(os.path.join(thumbnail_dir,hr[:2]+"_"+get_min(img)+"_"+os.path.split(img)[1]), cv2_img)
			
def move_videos(dt):
	vids = []
	for vid in  glob.iglob(dt_path+'/**/*.mp4', recursive=True):
		vids.append(vid)
	
	print("No. of videos to be moved are :"+str(len(vids)))
	if len(vids)!=0:
		ensure_dir_exists(stairs_target_vids_dir+dt)
		for vid in vids:
			hr = get_hour(vid)
			ensure_dir_exists(stairs_target_vids_dir+dt+"/"+hr)
			shutil.move(vid,stairs_target_vids_dir+dt+"/"+hr+"/"+os.path.split(vid)[1])
	
date_dirs = get_sub_dirs(stairs_root_dir)
print("\n\nRunning rearrange-stairs-photos at:"+datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
for dt in date_dirs:
	dt_path = stairs_root_dir+dt
	#print(dt_path)
		
	move_images(dt)
	move_videos(dt)

	
	
			
			
		

