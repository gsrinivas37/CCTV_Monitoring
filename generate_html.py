#!/usr/bin/python
import os.path
import os
import datetime

def get_files(parent_dir, extension):
    return [x for x in os.listdir(parent_dir) if x.endswith(extension)]

def generate_main_html(root_dir):
    dates_html_file = root_dir+"/index.html"
    f = open(dates_html_file, "w")
    f.write('<html><body>')

    for date_dir in get_sub_dirs(root_dir):
        f.write('<A href=\"./%s\">%s</A><br>'%(date_dir,date_dir))

    f.write('</body></html>')
    f.close()

def get_sub_dirs(root_dir):
    return [x for x in os.listdir(root_dir) if os.path.isdir(root_dir+"/"+x)]
    
def generate_hours_html_on_date(root_dir, date_dir):
    date_html = root_dir+"/"+date_dir+"/index.html"    
    f = open(date_html, "w")
    f.write('<html><body>')
    hours = get_sub_dirs(root_dir+"/"+date_dir)
    for hour_dir in hours:
        person_dir = os.path.join(root_dir,date_dir,hour_dir,"persons")
        if os.path.exists(person_dir):
            person_list = get_files(person_dir,"jpg")
            images_list = get_files(os.path.join(root_dir,date_dir,hour_dir),"jpg")
            f.write('<b>%s</b>&emsp;<A href=\"./%s/persons\">Person images(%d)</A>&emsp;<A href=\"./%s\"> All Images (%d)</A><br>'%(hour_dir,hour_dir,len(person_list),hour_dir,len(images_list)))
        else:
            f.write('<A href=\"./%s\">%s</A><br>'%(hour_dir,hour_dir))

    f.write('</body></html>')
    f.close()

def generate_img_html_on_date_hour(root_dir, date_dir,hour_dir):
    if not os.path.exists(os.path.join(root_dir,date_dir,hour_dir)):
        return
        
    hour_html = root_dir+"/"+date_dir+"/"+hour_dir+"/index.html"
    f = open(hour_html, "w")
    f.write('<html><style>img{border: 1px solid #ddd;border-radius: 4px; padding: 5px; width: 150px;} img:hover { box-shadow: 0 0 2px 1px rgba(0,140, 186, 0.5);} </style><body>')
    images = get_files(os.path.join(root_dir,date_dir,hour_dir),"jpg")
    for img_file in images:
        f.write('<a target=\"_blank\" href=\"./%s\"><img src=\"./%s\" alt=\"Forest\"></a>'%(img_file,img_file))
    f.write('</body></html>')
    f.close()
    
    #Generate HTML for persons directory
    person_dir = os.path.join(root_dir,date_dir,hour_dir,"persons")
    if os.path.exists(person_dir):
        person_list = get_files(person_dir,"jpg")
        hour_html = os.path.join(root_dir,date_dir,hour_dir,"persons","index.html")
        f = open(hour_html, "w")
        f.write('<html><style>img{border: 1px solid #ddd;border-radius: 4px; padding: 5px; width: 150px;} img:hover { box-shadow: 0 0 2px 1px rgba(0,140, 186, 0.5);} </style><body>')
        for img_file in person_list:
            f.write('<a target=\"_blank\" href=\"../%s\"><img src=\"./%s\" alt=\"Forest\"></a>'%(img_file,img_file))
        f.write('</body></html>')
        f.close()

def generate_vid_html_on_date_hour(root_dir, date_dir,hour_dir):
    if not os.path.exists(os.path.join(root_dir,date_dir,hour_dir)):
        return
    hour_html = root_dir+"/"+date_dir+"/"+hour_dir+"/index.html"
    f = open(hour_html, "w")
    f.write('<html><style>img{border: 1px solid #ddd;border-radius: 4px; padding: 5px; width: 150px;} img:hover { box-shadow: 0 0 2px 1px rgba(0,140, 186, 0.5);} </style><body>')
    vids = os.listdir(root_dir+"/"+date_dir+"/"+hour_dir)
    for vid in vids:
        if vid.endswith("mp4"):
            f.write('<a href=\"./%s\">%s</a><br>'%(vid,vid))
    f.write('</body></html>')
    f.close()
	
now = datetime.datetime.now()
date = now.strftime("%Y-%m-%d")

root_dir = "/mnt/hdd/GatePhotos"
generate_main_html(root_dir)
generate_hours_html_on_date(root_dir,date)
generate_img_html_on_date_hour(root_dir,date,'%02dhour'%(now.hour))
if now.hour != 0:
    generate_img_html_on_date_hour(root_dir,date,'%02dhour'%(now.hour-1))
    
root_dir = "/mnt/hdd/GateVideos"
generate_main_html(root_dir)
generate_hours_html_on_date(root_dir,date)
generate_vid_html_on_date_hour(root_dir,date,'%02dhour'%(now.hour))
if now.hour != 0:
    generate_vid_html_on_date_hour(root_dir,date,'%02dhour'%(now.hour-1))

root_dir = "/mnt/hdd/StairsPhotos"
generate_main_html(root_dir)
generate_hours_html_on_date(root_dir,date)
generate_img_html_on_date_hour(root_dir,date,'%02dhour'%(now.hour))
if now.hour != 0:
    generate_img_html_on_date_hour(root_dir,date,'%02dhour'%(now.hour-1))
    
root_dir = "/mnt/hdd/StairsVideos"
generate_main_html(root_dir)
generate_hours_html_on_date(root_dir,date)
generate_vid_html_on_date_hour(root_dir,date,'%02dhour'%(now.hour))
if now.hour != 0:
    generate_vid_html_on_date_hour(root_dir,date,'%02dhour'%(now.hour-1))

log_file = "/home/pi/www/logs/generate_html/log.txt"
str = ("HTML files are updated at %s\n")%(now.strftime("%Y-%m-%d %H:%M"))
f = open(log_file, "a")
f.write(str)
f.close()
