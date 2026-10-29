#!/bin/bash
echo "🚀 Initializing Multi-Asset Trading Nodes..."
nohup python3 -m streamlit run dashboard.py --server.port 8501 > dashboard_runtime.log 2>&1 &
echo "[+] Waiting for Streamlit UI dashboard server to initialize..."
sleep 5
for asset in XAUUSD WTI XAGUSD; do
    if [ -d "$asset" ]; then
        echo "[+] Launching computational background node for: $asset"
        cd "$asset"
        nohup python3 trader.py > runtime_log.txt 2>&1 &
        cd ..
    fi
done
chmod +x launch_tv.sh
./launch_tv.sh
