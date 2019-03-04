from shared import *

root_dir = '/mnt/hdd/GatePhotos'

today = datetime.datetime.now().strftime("%Y-%m-%d")
print(today)

for date_dir in get_sub_dirs(root_dir):
    if date_dir != today:
        save_space(os.path.join(root_dir,date_dir))