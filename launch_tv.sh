#!/bin/bash
export DISPLAY=:0
nohup streamlit run dashboard.py > dashboard_log.txt 2>&1 &
sleep 3
chromium-browser --noerrdialogs --disable-infobars --kiosk http://localhost:8501 > /dev/null 2>&1 &
