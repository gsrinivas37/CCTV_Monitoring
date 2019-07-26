import os
import time
import datetime

def measure_temp():
        temp = os.popen("vcgencmd measure_temp").readline()
        return (temp.replace("temp=",""))

cur_time = datetime.datetime.now()
temp_log = "/mnt/hdd/logs/temperature/log_"+cur_time.strftime("%Y-%m-%d")+".txt"
str = ("Temperature measured at %s is %s")% (cur_time.strftime("%Y-%m-%d %H:%M"), measure_temp())
print(str)

f = open(temp_log, "a")
f.write(str)
f.close()
