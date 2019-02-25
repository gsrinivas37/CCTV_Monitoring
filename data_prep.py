#!/usr/bin/python
from shared import *

dest_dir = "/mnt/hdd/train/GatePhotos"
root_dir = "/mnt/hdd/GatePhotos"
for date in get_sub_dirs(os.path.join(root_dir)):
    ensure_dir_exists(os.path.join(dest_dir,date))
    for hr_dir in get_sub_dirs(os.path.join(root_dir,date)):
        print("Images in "+hr_dir)
        ensure_dir_exists(os.path.join(dest_dir,date,hr_dir))
        person_dir = os.path.join(root_dir,date,hr_dir,"persons")
        person_dir_exists = os.path.exists(person_dir)
        for img in get_files(os.path.join(root_dir,date,hr_dir),"jpg"):
            print(os.path.join(root_dir,date,img))
            cv2_img = cv2.imread(os.path.join(root_dir,date,hr_dir, img))
            cv2_img = cv2.resize(cv2_img, (640, 360))
            person_img = os.path.join(person_dir, img)
            dest_path = os.path.join(dest_dir,date,hr_dir,img)
            if os.path.exists(person_img):
                dest_path = os.path.join(dest_dir,date,hr_dir,"p_"+img)
            cv2.imwrite(dest_path, cv2_img)
