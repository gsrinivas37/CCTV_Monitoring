#!/usr/bin/python
import os.path
import os
import datetime
import shutil

def addTitle(f, title):
    f.write('<title>%s</title>\n'%(title))
    f.write('<head><h1><center>%s</center></h1></head>\n'%(title))
    
def GetHumanReadable(size,precision=2):
    suffixes=['B','KB','MB','GB','TB']
    suffixIndex = 0
    while size > 1024 and suffixIndex < 4:
        suffixIndex += 1 #increment the index of the suffix
        size = size/1024.0 #apply the division
    return "%.*f %s"%(precision,size,suffixes[suffixIndex])

def get_files(parent_dir, extension):
    return [x for x in os.listdir(parent_dir) if x.endswith(extension)]

def generate_main_html(root_dir):
    dates_html_file = root_dir+"/index.html"
    f = open(dates_html_file, "w")
    f.write('<html>\n')
    addTitle(f,os.path.split(root_dir)[1])
    f.write('<body>\n')

    for date_dir in get_sub_dirs(root_dir)[::-1]:
        f.write('<h2><A href=\"./%s\">%s</A></h2>\n'%(date_dir,date_dir))

    f.write('</body>\n</html>')
    f.close()

def get_sub_dirs(root_dir):
    return [x for x in os.listdir(root_dir) if os.path.isdir(root_dir+"/"+x)]
    
def generate_hours_html_on_date(root_dir, date_dir):
    date_html = root_dir+"/"+date_dir+"/index.html"    
    f = open(date_html, "w")
    f.write('<html>\n')
    title = '%s (%s)'%(os.path.split(root_dir)[1],date_dir)
    addTitle(f, title)
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

def generate_img_html_on_date_hour(root_dir, date_dir,hour_dir):
    if not os.path.exists(os.path.join(root_dir,date_dir,hour_dir)):
        return
        
    hour_html = root_dir+"/"+date_dir+"/"+hour_dir+"/index.html"
    f = open(hour_html, "w")
    f.write('<html>\n<style>\nimg{border: 1px solid #ddd;border-radius: 4px; padding: 5px; width: 150px;} \nimg:hover { box-shadow: 0 0 2px 1px rgba(0,140, 186, 0.5);} \n</style>\n')
    title = '%s (%s) (%s)'%(os.path.split(root_dir)[1],date_dir, hour_dir)
    addTitle(f, title)
    f.write('<body>\n')
    images = get_files(os.path.join(root_dir,date_dir,hour_dir),"jpg")
    person_dir = os.path.join(root_dir,date_dir,hour_dir,"persons")
    if os.path.exists(person_dir):
        person_list = get_files(person_dir,"jpg")
        for p in person_list:
            images.remove(p)
    for img_file in images:
        thumbnail_file = os.path.join(root_dir,date_dir,hour_dir,"thumbnails",img_file)
        if os.path.exists(thumbnail_file):
            f.write('<a target=\"_blank\" href=\"./%s\"><img src=\"./thumbnails/%s\" alt=\"Forest\"></a>\n'%(img_file,img_file))
        else:
            f.write('<a target=\"_blank\" href=\"./%s\"><img src=\"./%s\" alt=\"Forest\"></a>\n'%(img_file,img_file))
    f.write('</body>\n</html>')
    f.close()
    
    #Generate HTML for persons directory
    if os.path.exists(person_dir):
        person_list = get_files(person_dir,"jpg")
        hour_html = os.path.join(root_dir,date_dir,hour_dir,"persons","index.html")
        f = open(hour_html, "w")
        f.write('<html>\n<style>\nimg{border: 1px solid #ddd;border-radius: 4px; padding: 5px; width: 150px;} \nimg:hover { box-shadow: 0 0 2px 1px rgba(0,140, 186, 0.5);} \n</style>\n')
        title = '%s (%s) (%s)'%(os.path.split(root_dir)[1],date_dir, hour_dir)
        addTitle(f, title)
        f.write('<body>\n')
        for img_file in person_list:
            f.write('<a target=\"_blank\" href=\"../%s\"><img src=\"./%s\" alt=\"Forest\"></a>\n'%(img_file,img_file))
        f.write('</body>\n</html>')
        f.close()

def generate_vid_html_on_date_hour(root_dir, date_dir,hour_dir):
    if not os.path.exists(os.path.join(root_dir,date_dir,hour_dir)):
        return
    hour_html = root_dir+"/"+date_dir+"/"+hour_dir+"/index.html"
    f = open(hour_html, "w")
    f.write('<html>\n')
    title = '%s (%s) (%s)'%(os.path.split(root_dir)[1],date_dir, hour_dir)
    addTitle(f, title)
    f.write('<body>\n')
    vids = os.listdir(root_dir+"/"+date_dir+"/"+hour_dir)
    for vid in vids:
        if vid.endswith("mp4"):
            size = os.path.getsize(os.path.join(root_dir,date_dir,hour_dir,vid))
            f.write('<h2><a href=\"./%s\">%s</a> (%s)</h2>'%(vid,vid,GetHumanReadable(size)))
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

time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
total, used, free = shutil.disk_usage("/mnt/hdd")
storage = '%d%% Full (%d GB Available)'%((used/total)*100,free// (2**30))

f = open("/home/pi/CCTV_Monitoring/index.html", "r")
out = open("/home/pi/www/index.html","w")
html = (f.read())
html = (html%(time,storage))
out.write(html)

f = open("/home/pi/CCTV_Monitoring/log_index.html", "r")
out = open("/home/pi/www/logs/index.html","w")
html = (f.read())

row = open("/home/pi/CCTV_Monitoring/row.html", "r")
row_temp = (row.read())
row_str = ""
for log in get_files("/home/pi/www/logs/gate","txt"):
    row_str.append(row_temp%(log[4:]))

html = (html%(row_str))
out.write(html)

print("Generate html ran at:"+time)
