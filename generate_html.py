#!/usr/bin/python
import os.path
import os
import datetime
import shutil

photo_root_dirs = ["/mnt/hdd/GatePhotos", "/mnt/hdd/StairsPhotos"]
video_root_dirs = ["/mnt/hdd/GateVideos", "/mnt/hdd/StairsVideos"]

def addTitle(f, main, dt="", hr="", personDir = None):
    title = main
    link = '<a href=\"../\">%s</a>'%(main)
    if dt!="":
        title = '%s (%s)'%(title,dt)
        if personDir == "Persons":
            link = '<a href=\"../../../\">%s</a> (%s) </a>'%(main, dt)
        else:
            link = '<a href=\"../../\">%s</a> (%s) </a>'%(main, dt)
    if dt!="" and hr!="":
        title = '%s (%s)'%(title,hr)
        if personDir == "Persons":
            link = '<a href=\"../../../../\">%s</a>&nbsp<a href=\"../../\">(%s)</a> (%s) (%s)&nbsp<a href=\"../\">(O)</a></a>'%(main, dt, hr,personDir)
        elif personDir == "Other":
            link = '<a href=\"../../../\">%s</a>&nbsp<a href=\"../\">(%s)</a> (%s) (%s)</a>&nbsp<a href="./persons">(P)</a>'%(main, dt, hr, personDir)
        elif personDir==None:
            link = '<a href=\"../../../\">%s</a>&nbsp<a href=\"../\">(%s)</a> (%s) </a>'%(main, dt, hr)
        else:
            link = '<a href=\"../../../\">%s</a>&nbsp<a href=\"../\">(%s)</a> (%s) (%s)</a>'%(main, dt, hr, personDir)

    if personDir!=None:
        title = '%s (%s)'%(title, personDir)
    f.write('<title>%s</title>\n'%(title))
    f.write('<head><h1><center>%s</center></h1></head>\n'%(link))
    
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

def generate_links(root_dir, date_dir,hour_dir, f, isPersonDir = False):
    isPhotoDir = "Photos" in os.path.split(root_dir)[1]
    isGateDir = "Gate" in os.path.split(root_dir)[1]
    f.write('<h2>')
    prev_link = None
    prev_hour = None
    next_link = None
    next_hour = None
    if hour_dir != "00hour":
        prev_hour = '%02dhour'%(int(hour_dir[0:2])-1)
        person_dir = os.path.join(root_dir,date_dir,prev_hour,"persons")
        if isPhotoDir and os.path.exists(person_dir):
            prev_link = "../"+prev_hour+"/persons"
        else:
            prev_link = "../"+prev_hour
        
        if isPersonDir == True:
            prev_link = "../"+prev_link

    if hour_dir != "23hour":
        next_hour = '%02dhour'%(int(hour_dir[0:2])+1)
        person_dir = os.path.join(root_dir,date_dir,next_hour,"persons")
        if isPhotoDir and os.path.exists(person_dir):
            next_link = "../"+next_hour+"/persons"
        else:
            other_dir = os.path.join(root_dir,date_dir,next_hour)
            if os.path.exists(other_dir):
                next_link = "../"+next_hour
        if next_link!=None and isPersonDir == True:
            next_link = "../"+next_link

    str1 = "Photos" if isPhotoDir else "Videos"
    str2 = "Videos" if isPhotoDir else "Photos"
    other_link = "../../../"+os.path.split(root_dir)[1].replace(str1,str2)+"/"+date_dir+"/"+hour_dir
    if isPersonDir == True:
        other_link = "../"+other_link

    if str1 == "Videos":
        other_person_dir = os.path.join(root_dir.replace(str1,str2),date_dir,hour_dir,"persons")
        if os.path.exists(other_person_dir):
            other_link = other_link+"/persons"

    str3 = "Gate" if isGateDir else "Stairs"
    str4 = "Stairs" if isGateDir else "Gate"
    othercam_link = "../../../"+os.path.split(root_dir)[1].replace(str3,str4)+"/"+date_dir+"/"+hour_dir
    othercam_person_dir = os.path.join(root_dir.replace(str3,str4),date_dir,hour_dir,"persons")
    if os.path.exists(othercam_person_dir):
        othercam_link = othercam_link+"/persons"

    if isPersonDir == True:
        othercam_link = "../"+othercam_link

    f.write('<h2>')
    if prev_link !=None:
        f.write('<div style=\"float: left\"><a href=\"%s\"> Previous</a> (%s)</div>'%(prev_link, prev_hour))
    if next_link !=None:
        f.write('<div style=\"float: right\"><a href=\"%s\"> Next</a> (%s)</div>'%(next_link, next_hour))

    f.write('<div style=\"margin: auto; width: 150px;\"><a href=\"%s\">%s</a>&emsp;&emsp;<a href=\"%s\">%s</a></div>'%(other_link,str2,othercam_link,str4))
    f.write('</h2>')

def generate_img_html_on_date_hour(root_dir, date_dir,hour_dir):
    if not os.path.exists(os.path.join(root_dir,date_dir,hour_dir)):
        return
    
    print('Generating %s HTML on %s at %s'%(os.path.split(root_dir)[1],date_dir,hour_dir))
    hour_html = root_dir+"/"+date_dir+"/"+hour_dir+"/index.html"
    f = open(hour_html, "w")
    f.write('<html>\n<style>\nimg{border: 1px solid #ddd;border-radius: 4px; padding: 5px; width: 150px;} \nimg:hover { box-shadow: 0 0 2px 1px rgba(0,140, 186, 0.5);} \n</style>\n')
    person_dir = os.path.join(root_dir,date_dir,hour_dir,"persons")
    per_dir = "Other" if os.path.exists(person_dir) else "All"
    addTitle(f, os.path.split(root_dir)[1],date_dir, hour_dir, personDir = per_dir)
    f.write('<body>\n')

    generate_links(root_dir, date_dir,hour_dir,f)
    images = get_files(os.path.join(root_dir,date_dir,hour_dir),"jpg")
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
        addTitle(f, os.path.split(root_dir)[1],date_dir, hour_dir, personDir = "Persons")
        f.write('<body>\n')
        generate_links(root_dir, date_dir,hour_dir,f, isPersonDir = True)
        for img_file in person_list:
            f.write('<a target=\"_blank\" href=\"../%s\"><img src=\"./%s\" alt=\"Forest\"></a>\n'%(img_file,img_file))
        f.write('</body>\n</html>')
        f.close()

def generate_vid_html_on_date_hour(root_dir, date_dir,hour_dir):
    if not os.path.exists(os.path.join(root_dir,date_dir,hour_dir)):
        return

    print('Generating %s HTML on %s at %s'%(os.path.split(root_dir)[1],date_dir,hour_dir))
    
    hour_html = root_dir+"/"+date_dir+"/"+hour_dir+"/index.html"
    f = open(hour_html, "w")
    f.write('<html>\n')
    addTitle(f, os.path.split(root_dir)[1],date_dir, hour_dir)
    f.write('<body>\n')
    generate_links(root_dir, date_dir,hour_dir,f)
    vids = os.listdir(root_dir+"/"+date_dir+"/"+hour_dir)
    for vid in vids:
        if vid.endswith("mp4"):
            size = os.path.getsize(os.path.join(root_dir,date_dir,hour_dir,vid))
            f.write('<h2><a href=\"./%s\">%s</a> (%s)</h2>'%(vid,vid,GetHumanReadable(size)))
    f.write('</body></html>')
    f.close()

def generate_at_time(now,generate_hours_html=False):
    cur_hour = '%02dhour'%(now.hour)
    date = now.strftime("%Y-%m-%d")
    print("Generate at time: "+ str(now))

    for root_dir in photo_root_dirs:
        if generate_hours_html == True:
            generate_hours_html_on_date(root_dir,date)
        generate_img_html_on_date_hour(root_dir,date,cur_hour)
    for root_dir in video_root_dirs:
        if generate_hours_html == True:
            generate_hours_html_on_date(root_dir,date)
        generate_vid_html_on_date_hour(root_dir,date,cur_hour)

def generate_for_hours(hrs=2):
    now = datetime.datetime.now()
    generate_at_time(now, generate_hours_html=True)
    hr = 1
    while(hr<=hrs):
        now = datetime.datetime.now() - datetime.timedelta(hours=hr)
        generate_at_time(now)
        hr = hr + 1

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

time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
total, used, free = shutil.disk_usage("/mnt/hdd")
storage = '%d%% Full (%d GB Available)'%((used/total)*100,free// (2**30))

row_str = ""
for dt in get_sub_dirs("/mnt/hdd/GatePhotos")[::-1]:
    row_str+= "<tr>\n"
    row_str+= ("<td><h2><a href='./GatePhotos/%s'> %s </a></h2></td>\n"%(dt,dt))
    if os.path.exists("/mnt/hdd/StairsPhotos/"+dt): 
        row_str+= ("<td><h2><a href='./StairsPhotos/%s'> %s </a></h2></td>\n"%(dt,dt))
    else:
        row_str+= "<td><h2>Not Available</h2></td>"
    if os.path.exists("/mnt/hdd/GateVideos/"+dt): 
        row_str+= ("<td><h2><a href='./GateVideos/%s'> %s </a></h2></td>\n"%(dt,dt))
    else:
        row_str+= "<td><h2>Not Available</h2></td>"
    if os.path.exists("/mnt/hdd/StairsVideos/"+dt): 
        row_str+= ("<td><h2><a href='./StairsVideos/%s'> %s </a></h2></td>\n"%(dt,dt))
    else:
        row_str+= "<td><h2>Not Available</h2></td>"
    row_str+="</tr>\n"

f = open("/home/pi/CCTV_Monitoring/index.html", "r")
out = open("/home/pi/www/index.html","w")
html = (f.read())
html = (html%(time,storage,row_str))
out.write(html)

f = open("/home/pi/CCTV_Monitoring/log_index.html", "r")
out = open("/home/pi/www/logs/index.html","w")
html = (f.read())

row = open("/home/pi/CCTV_Monitoring/row.html", "r")
row_temp = (row.read())
row_str = ""
logs = get_files("/home/pi/www/logs/gate","txt")
logs.sort(reverse=True)
for log in logs:
    dt = log[4:-4] 
    temp=(row_temp%(dt,dt,dt,dt,dt,dt,dt,dt,dt,dt))
    row_str+=temp

html = (html%(row_str))
out.write(html)
print("\n")
