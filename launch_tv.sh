#!/bin/bash
export DISPLAY=:0
echo "📺 Redirecting display output to TV HDMI interface..."
sleep 1
chromium --user-data-dir=/home/robhuzzey/.config/chromium-tv --noerrdialogs --disable-infobars --password-store=basic --kiosk http://localhost:8501 &
echo "🎉 Fullscreen Kiosk Engine projected onto TV monitor."
