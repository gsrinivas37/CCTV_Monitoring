import os
import time
import datetime

def measure_temp():
        temp = os.popen("vcgencmd measure_temp").readline()
        return (temp.replace("temp=",""))

temp_log = "/home/pi/www/logs/temperature/log.txt"
cur_time = datetime.datetime.now()
str = ("Temperature measured at %s is %s")% (cur_time.strftime("%Y-%m-%d %H:%M"), measure_temp())
print(str)

f = open(temp_log, "a")
f.write(str)
f.close()