import datetime
import os

cur_time = datetime.datetime.now()
temp_log = "/home/pi/www/logs/hdd_status/log_"+cur_time.strftime("%Y-%m-%d")+".txt"
time = cur_time.strftime("%Y-%m-%d %H:%M")
st = "\n"+time+": "
f = open(temp_log, "a")
try:
    os.listdir("/mnt/hdd")
    f.write(st+"Good")
except Exception as error:
    f.write(st+str(error))
f.close()
