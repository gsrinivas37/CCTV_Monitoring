#!/bin/sh
status=`wget -O - --server-response http://login.hireachbroadband.com  2>&1 | awk '/^  Location:/{print $2}'`
if [[ "$status" == *login ]]; then
    wget  -O - --quiet --post-data 'user=g_narahari&password=123456' http://login.hireachbroadband.com/login
    status=`wget -O - --server-response http://login.hireachbroadband.com  2>&1 | awk '/^  Location:/{print $2}'`
    if [[ "$status" == *login ]]; then
	if [ ! -f /home/pi/www/logs/internet_autologin/nonet ]; then
	    echo "No internet at $(date)" >> /home/pi/www/logs/internet_autologin/log.txt
	    touch /home/pi/www/logs/internet_autologin/nonet
	fi
    else
        echo "Auto logged on $(date)" >> /mnt/hdd/logs/internet_autologin/log.txt
	rm /home/pi/www/logs/internet_autologin/nonet
    fi
fi
