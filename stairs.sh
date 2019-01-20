#!/bin/bash
python3 /home/pi/CCTV_Monitoring/rearrange_stairs_footage.py &>> /home/pi/www/logs/stairs/log_$(date +%F).txt
