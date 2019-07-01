#!/usr/bin/python
import os.path
from shared import *


def generate_at_time(time,generate_hours_html=False):
    cur_hour = '%02dhour'%(time.hour)
    date = time.strftime("%Y-%m-%d")
    for root_dir in photo_root_dirs:
        if generate_hours_html == True:
            generate_hours_html_on_date(root_dir,date)
        generate_img_html_on_date_hour(root_dir,date,cur_hour)
    for root_dir in video_root_dirs:
        if generate_hours_html == True:
            generate_hours_html_on_date(root_dir,date)
        generate_vid_html_on_date_hour(root_dir,date,cur_hour)


def generate_for_hours(hrs=3):
    for hr in range(hrs):
        now = datetime.datetime.now() - datetime.timedelta(hours=hr)
        generate_at_time(now, generate_hours_html= (hr==0))


def generate_all():
    for root_dir in photo_root_dirs:
        for dt_dir in get_sub_dirs(root_dir):
            generate_hours_html_on_date(root_dir,dt_dir)
            for hr_dir in get_sub_dirs(os.path.join(root_dir,dt_dir)):
                generate_img_html_on_date_hour(root_dir,dt_dir,hr_dir)

    for root_dir in video_root_dirs:
        for dt_dir in get_sub_dirs(root_dir):
            generate_hours_html_on_date(root_dir,dt_dir)
            for hr_dir in get_sub_dirs(os.path.join(root_dir,dt_dir)):
                generate_vid_html_on_date_hour(root_dir,dt_dir,hr_dir)

generate_for_hours()
#generate_all()
generate_front_page()
