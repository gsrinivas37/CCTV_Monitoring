from shared import *

import tarfile

def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

def backup(root_dir,tar_file):
    target_dir = "/mnt/hdd/"+ os.path.basename(root_dir)
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

    print("Creating tar file...")
    make_tarfile(tar_file,os.path.join(target_dir))
    print("Deleting files...")
    shutil.rmtree(target_dir)

gate_root_dir = os.path.join(photo_root_dirs[0],"2019-07-13")
backup(gate_root_dir,"/mnt/hdd/gate.tar.gz")

stairs_root_dir = os.path.join(photo_root_dirs[1],"2019-07-13")
backup(stairs_root_dir,"/mnt/hdd/stairs.tar.gz")