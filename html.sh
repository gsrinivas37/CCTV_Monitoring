#!/bin/bash
python3 /home/pi/CCTV_Monitoring/generate_html.py &>> /home/pi/www/logs/html/log_$(date +%F).txt
