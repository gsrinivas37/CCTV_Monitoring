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