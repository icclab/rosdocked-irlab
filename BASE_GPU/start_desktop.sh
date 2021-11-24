#!/bin/bash

# Start XVnc/X/Lubuntu
chmod -f 777 /tmp/.X11-unix
# From: https://superuser.com/questions/806637/xauth-not-creating-xauthority-file (squashes complaints about .Xauthority)
touch ~/.Xauthority
xauth generate :0 . trusted

# read VNC passwd from ENV variable, prompt for passwd if not set
if [[ -z "${VNC_PASSWORD}" ]]; then
    echo "VNC password not provided as environmental variable VNC_PASSWORD. Will be prompted"	
    /opt/TurboVNC/bin/vncserver -SecurityTypes vnc
else
    echo "VNC password provided as environmental variable VNC_PASSWORD. Will be saved"
    echo "${VNC_PASSWORD}" | vncpasswd -f > ~/.vnc/passwd
    chmod 600 ~/.vnc/passwd
    /opt/TurboVNC/bin/vncserver -rfbauth /home/ros/.vnc/passwd -SecurityTypes vnc
fi

# Start NoVNC. self.pem is a self-signed cert.
if [ $? -eq 0 ] ; then
    sudo /opt/noVNC/utils/launch.sh --vnc localhost:5901 --cert /home/ros/self.pem --listen 443;
fi
