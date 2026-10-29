#!/bin/bash
echo "Launching system..."
for d in XAUUSD WTI XAGUSD; do
    cd $d && nohup python3 trader.py > runtime_log.txt 2>&1 &
    cd ..
done
./launch_tv.sh
