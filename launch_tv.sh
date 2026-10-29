#!/bin/bash
export DISPLAY=:0
echo "📺 Calibrating layout proportions for 50-Inch TV Monitor (1.25x Scaling)..."
sleep 1
chromium --force-device-scale-factor=1.25 --noerrdialogs --disable-infobars --password-store=basic --kiosk http://localhost:8501 &
echo "🎉 Premium grid scale factor deployed."
