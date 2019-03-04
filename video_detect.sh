#!/bin/bash
python3 /home/pi/CCTV_Monitoring/video_detect.py &>> /home/pi/www/logs/person_detect/log_$(date +%F).txt
