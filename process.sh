#!/bin/bash
python3 /home/pi/CCTV_Monitoring/process_footage.py &>> /home/pi/www/logs/process/log_$(date +%F).txt
