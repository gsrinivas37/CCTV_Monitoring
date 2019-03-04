from shared import *

gate_video_dir = '/mnt/hdd/GateVideos'
stairs_video_dir = '/mnt/hdd/StairsVideos'

def check_person_exists_in_video(root_dir, date, hour, video):
    root_dir = root_dir.replace("Videos","Photos")
    temp = video.split('[M]')[0].split('-')
    start_time = datetime.datetime.strptime(date + " " + temp[0], '%Y-%m-%d %H.%M.%S')
    end_time = datetime.datetime.strptime(date + " " + temp[1], '%Y-%m-%d %H.%M.%S')

    person_dir = os.path.join(root_dir,date,hour,'persons')
    imgs = get_files(person_dir,"jpg")
    imgs.sort()
    for i in range(len(imgs)):
        time = imgs[i].split('[M]')[0]
        if "_" in time:
            img_time = datetime.datetime.strptime(date + " " + time, '%Y-%m-%d %H_%M_%S')
        else:
            img_time = datetime.datetime.strptime(date + " " + time, '%Y-%m-%d %H.%M.%S')
        if img_time > start_time:
            return img_time < end_time
    return False

def run_on_date(date):
    print("Running on date:"+date)
    if os.path.exists(os.path.join(gate_video_dir,date)):
        for hr_dir in get_sub_dirs(os.path.join(gate_video_dir,date)):
            for video in get_files(os.path.join(gate_video_dir,date,hr_dir),"mp4"):
                exists = check_person_exists_in_video(gate_video_dir, date, hr_dir, video)
                if exists==False:
                    os.remove(os.path.join(gate_video_dir,date,hr_dir,video))

    if os.path.exists(os.path.join(stairs_video_dir, date)):
        for hr_dir in get_sub_dirs(os.path.join(stairs_video_dir,date)):
            for video in get_files(os.path.join(stairs_video_dir,date,hr_dir),"mp4"):
                exists = check_person_exists_in_video(stairs_video_dir, date, hr_dir, video)
                if exists==False:
                    os.remove(os.path.join(stairs_video_dir,date,hr_dir,video))

today = datetime.datetime.now().date()

for dt_dir in get_sub_dirs(gate_video_dir):
    dt = datetime.datetime.strptime(dt_dir, "%Y-%m-%d").date()
    elapsed_days = (today - dt).days
    if elapsed_days > 5:
        run_on_date(dt_dir)
