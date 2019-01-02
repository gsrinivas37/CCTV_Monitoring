# CCTV_Monitoring
CCTV Monitoring project using a raspberry pi, two IP cameras and an external hard disk



*/5 * * * * python3 rearrange_stairs_footage.py
*/5 * * * * python3 rearrange_gate_footage.py
*/5 * * * * (sleep 30; python3 generate_html.py)
*/30 * * * * python measure_temperature.py
2 * * * * python3 cctv_human_detection.py
*/1 * * * * bash internet_autologin.sh
0 2 * * * python delete_old_footage.py
