#!/usr/bin/python
import os.path
import os
import datetime
import shutil
import cv2
import glob
from shared import ensure_dir_exists

def create_dirs(file):
    if not os.path.isdir(file):
        create_dirs(os.path.dirname(file))

    if os.path.exists(os.path.dirname(file)) and not os.path.exists(file) and not os.path.isfile(file):
        os.mkdir(file)

ROOT_DIR = 'C:\\Users\\sgudla\\Downloads\\1'
TARGET_DIR = 'C:\\Users\\sgudla\\Downloads\\train\\1'
for img in glob.iglob(ROOT_DIR+'/**/*.jpg', recursive=True):
    cv2_img = cv2.imread(img)
    crop_img = cv2_img[0:120, 180:360]
    dest = img.replace(ROOT_DIR,TARGET_DIR)
    create_dirs(os.path.split(dest)[0])
    cv2.imwrite(dest,crop_img)



