import os
import datetime
import shutil

expiry_date_dictionary = {
  "/mnt/hdd/GatePhotos": 45,
  "/mnt/hdd/StairsPhotos": 45,
  "/mnt/hdd/GateVideos": 25,
  "/mnt/hdd/StairsVideos": 20,
  "/mnt/hdd/tmp/GateCamera": 0,
  "/mnt/hdd/tmp/StairsCamera": 0
}

def get_sub_dirs(root_dir):
    return [x for x in os.listdir(root_dir) if os.path.isdir(root_dir+"/"+x)]

today = datetime.datetime.now().date()
for root_dir in expiry_date_dictionary:
    expiry_date = expiry_date_dictionary[root_dir]
    for dt_dir in get_sub_dirs(root_dir):
        dt = datetime.datetime.strptime(dt_dir, "%Y-%m-%d").date()
        elapsed_days = (today-dt).days
        if elapsed_days > expiry_date:
            shutil.rmtree(root_dir+"/"+dt_dir)


