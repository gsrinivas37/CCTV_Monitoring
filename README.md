# CCTV_Monitoring
CCTV Monitoring project using a raspberry pi, two IP cameras and an external hard disk



*/5 * * * * python3 rearrange_stairs_footage.py<br>
*/5 * * * * python3 rearrange_gate_footage.py<br>
*/5 * * * * (sleep 30; python3 generate_html.py)<br>
*/30 * * * * python measure_temperature.py<br>
2 * * * * python3 cctv_human_detection.py<br>
*/1 * * * * bash internet_autologin.sh<br>
0 2 * * * python delete_old_footage.py<br>
