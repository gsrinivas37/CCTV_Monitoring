#!/bin/bash
python3 /home/pi/CCTV_Monitoring/rearrange_gate_footage.py &>> /home/pi/www/logs/gate/log_$(date +%F).txt
