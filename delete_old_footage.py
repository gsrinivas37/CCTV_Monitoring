import os
import datetime
import shutil
from shared import get_sub_dirs

expiry_date_dictionary = {
  "/mnt/hdd/GatePhotos": 5,
  "/mnt/hdd/StairsPhotos": 5,
  "/mnt/hdd/GateVideos": 3,
  "/mnt/hdd/StairsVideos": 3,
  "/mnt/hdd/tmp/GateCamera": 0,
  "/mnt/hdd/tmp/StairsCamera": 0
}

today = datetime.datetime.now().date()
for root_dir in expiry_date_dictionary:
    expiry_date = expiry_date_dictionary[root_dir]
    for dt_dir in get_sub_dirs(root_dir):
        if dt_dir == "train":
            continue
        dt = datetime.datetime.strptime(dt_dir, "%Y-%m-%d").date()
        elapsed_days = (today-dt).days
        if elapsed_days > expiry_date:
            try:
		shutil.rmtree(root_dir+"/"+dt_dir)
	    except:
		print("Error deleting directory:"+root_dir+"/"+dt_dir)


