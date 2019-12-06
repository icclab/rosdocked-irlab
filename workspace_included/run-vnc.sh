#!/bin/bash
if [[ $# -ne 1 ]]; then
    echo "Illegal number of parameters"
    echo "usage: ./run-vnc.sh <vnc_password>"
    exit 2
fi

echo "----- Starting virtual screen -----"
Xvfb :0 -screen 0 1920x1080x16  &
sleep 3

echo "----- Strting VNC -----"
x11vnc --passwd $1 &
sleep 3

echo "----- Starting fluxbox -----"
fluxbox &
sleep 3

echo "----- Starting novnc -----"
cd /opt/novnc/utils
sudo openssl req -newkey rsa:2048 -new -nodes -x509 -days 3650 \
       -subj "/C=CH" \
       -keyout key.pem -out self.pem
sleep 3
cat key.pem | sudo tee -a self.pem
sudo ./launch.sh  --listen 443 --ssl-only &
