#!/bin/bash
echo "============================================================"
echo "    🤖 HERMES QUANT CORE SYSTEM INSTALLER (HEADLESS)"
echo "============================================================"
mkdir -p ~/.config
echo -e "[idle]\nscreensaver_timeout = -1\ndpms_timeout = -1" > ~/.config/wayfire.ini
echo "[+] Disabling Wayland/Wayfire TV screen blanking sleep... Done."

read -p "👉 Enter your OpenAI Secret API Key (sk-...): " openai_key
read -p "👉 Enter your Pepperstone Account Login ID: " pepper_id
read -p "👉 Enter your Pepperstone Account Password: " pepper_pass
read -p "👉 Enter your Pepperstone Server Name: " pepper_server

echo "export OPENAI_API_KEY=\"$openai_key\"" >> ~/.bashrc
echo "export PEPPERSTONE_ID=\"$pepper_id\"" >> ~/.bashrc
echo "export PEPPERSTONE_PASS=\"$pepper_pass\"" >> ~/.bashrc
echo "export PEPPERSTONE_SERVER=\"$pepper_server\"" >> ~/.bashrc

echo "[+] Setup Complete. Please run 'source ~/.bashrc' then './run_system.sh'"
