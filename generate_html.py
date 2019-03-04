#!/usr/bin/python
import os.path
from shared import *

def generate_hours_html_on_date(root_dir, date_dir):
    if not os.path.exists(root_dir+"/"+date_dir):
        return 
    date_html = root_dir+"/"+date_dir+"/index.html"    
    f = open(date_html, "w")
    f.write('<html>\n')
    addTitle(f, os.path.split(root_dir)[1],date_dir)
    f.write('<body>\n')
    hours = get_sub_dirs(root_dir+"/"+date_dir)
    for hour_dir in hours[::-1]:
        person_dir = os.path.join(root_dir,date_dir,hour_dir,"persons")
        if os.path.exists(person_dir):
            person_list = get_files(person_dir,"jpg")
            images_list = get_files(os.path.join(root_dir,date_dir,hour_dir),"jpg")
            f.write('<h2>%s&emsp;<A href=\"./%s/persons\">Person images(%d)</A>&emsp;<A href=\"./%s\"> Other Images (%d)</A></h2>\n'%(hour_dir,hour_dir,len(person_list),hour_dir,len(images_list)-len(person_list)))
        else:
            images_list = get_files(os.path.join(root_dir,date_dir,hour_dir),"jpg")
            currenthour = '%02dhour'%(datetime.datetime.now().hour)
            if len(images_list) == 0:
                video_list = get_files(os.path.join(root_dir,date_dir,hour_dir),"mp4")
                f.write('<h2><A href=\"./%s\">%s</A> (%d Videos)</h2>'%(hour_dir,hour_dir,len(video_list)))
            else:
                if hour_dir==currenthour:
                    f.write('<h2><A href=\"./%s\">%s</A> (%d Images. Person detection will happen at the end of hour)</h2>\n'%(hour_dir,hour_dir,len(images_list)))
                else:
                    f.write('<h2><A href=\"./%s\">%s</A> (%d Images with no persons)</h2>\n'%(hour_dir,hour_dir,len(images_list)))

    f.write('</body>\n</html>')
    f.close()

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
