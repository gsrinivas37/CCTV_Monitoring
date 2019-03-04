from shared import *

past_time = datetime.datetime.now() - datetime.timedelta(days=4)
past_date = past_time.strftime("%Y-%m-%d")

for photo_root in photo_root_dirs:
    date_dir = os.path.join(photo_root, past_date)
    if os.path.exists(date_dir):
        save_space_video(date_dir)
        save_space_image(date_dir)

for video_root in video_root_dirs:
    date_dir = os.path.join(video_root,past_date)
    if os.path.exists(date_dir):
        save_video_space2(date_dir)
        generate_hours_html_on_date(video_root,past_date)
        for hr_dir in get_sub_dirs(date_dir):
            generate_vid_html_on_date_hour(video_root, past_date, hr_dir)

