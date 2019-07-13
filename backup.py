from shared import *

def backup(date):
    root_dir = photo_root_dirs[0]+date
    target_dir = "/mnt/hdd/"+date
    ensure_dir_exists(target_dir)
    hours = get_sub_dirs(root_dir)
    for hour_dir in hours:
        ensure_dir_exists(os.path.join(target_dir,hour_dir))
        images_list = get_files(os.path.join(root_dir,hour_dir),"jpg")
        person_dir = os.path.join(root_dir,hour_dir,"persons")
        if os.path.exists(person_dir):
            person_list = get_files(person_dir,"jpg")
            for p in person_list:
                print("Copy full image:"+p)
                images_list.remove(p)
        for img in images_list:
            print("Copy thumbnail image:"+img)


backup("2019-07-13")