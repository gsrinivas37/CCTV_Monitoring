from shared import *

def backup(date):
    root_dir = os.path.join(photo_root_dirs[0],date)
    target_dir = "/mnt/hdd/"+date
    ensure_dir_exists(target_dir)
    hours = get_sub_dirs(root_dir)
    for hour_dir in hours:
        ensure_dir_exists(os.path.join(target_dir,hour_dir))
        person_dir = os.path.join(root_dir,hour_dir,"persons")
        thumbnail_dir = os.path.join(root_dir,hour_dir,"thumbnails")
        shutil.copytree(thumbnail_dir,os.path.join(target_dir,hour_dir,"thumbnails"))
        if os.path.exists(person_dir):
            person_list = get_files(person_dir,"jpg")
            print("Copying full images in "+hour_dir+" Total images: "+str(len(person_list)))
            for p in person_list:
                shutil.copy(os.path.join(root_dir,hour_dir,p),os.path.join(target_dir,hour_dir,p))

backup("2019-07-13")