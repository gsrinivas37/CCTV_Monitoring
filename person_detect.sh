#!/bin/bash
python3 /home/pi/CCTV_Monitoring/cctv_human_detection.py &>> /home/pi/www/logs/person_detect/log_$(date +%F).txt
