from shared import *

import tarfile

def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

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
                os.remove(os.path.join(target_dir,hour_dir,"thumbnails",p))
                shutil.copy(os.path.join(root_dir,hour_dir,p),os.path.join(target_dir,hour_dir,p))

    make_tarfile("/mnt/hdd/gate.tar.gz",os.path.join(target_dir))

backup("2019-07-13")