#!/usr/bin/python
from shared import *
import datetime
dest_dir = "/mnt/hdd/train/GatePhotos"
root_dir = "/mnt/hdd/GatePhotos"
dt_dirs = ["2019-01-01",
"2019-01-12",
"2019-01-13",
"2019-01-14",
"2019-01-15",
"2019-01-16",
"2019-01-17",
"2019-01-18",
"2019-01-19"
]
feb7 = datetime.datetime.strptime("2019-02-12","%Y-%m-%d").date()
for date in get_sub_dirs(os.path.join(root_dir)):
    dt = datetime.datetime.strptime(date,"%Y-%m-%d").date()
    if (dt-feb7).days <= 0:
        continue
    ensure_dir_exists(os.path.join(dest_dir,date))
    print("Images in "+date)
    for hr_dir in get_sub_dirs(os.path.join(root_dir,date)):
        print("Images in "+hr_dir)
        ensure_dir_exists(os.path.join(dest_dir,date,hr_dir))
        person_dir = os.path.join(root_dir,date,hr_dir,"persons")
        person_dir_exists = os.path.exists(person_dir)
        for img in get_files(os.path.join(root_dir,date,hr_dir),"jpg"):
            img_path = os.path.join(root_dir,date,img)
            try: 
                cv2_img = cv2.imread(os.path.join(root_dir,date,hr_dir, img))
                cv2_img = cv2.resize(cv2_img, (640, 360))
                person_img = os.path.join(person_dir, img)
                dest_path = os.path.join(dest_dir,date,hr_dir,img)
                if os.path.exists(person_img):
                    dest_path = os.path.join(dest_dir,date,hr_dir,"p_"+img)
                cv2.imwrite(dest_path, cv2_img)
            except:
                print("error saving:"+img_path)
