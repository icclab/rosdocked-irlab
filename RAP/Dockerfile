ARG BASE_IMAGE
FROM $BASE_IMAGE 

RUN sudo apt update && \
    sudo apt install -y iputils-ping dnsutils xfce4-terminal
    
# install Ms vscode
RUN wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /tmp/packages.microsoft.gpg && \
    sudo install -o root -g root -m 644 /tmp/packages.microsoft.gpg /etc/apt/trusted.gpg.d/ && \
    sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/trusted.gpg.d/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list' && \
    sudo apt install apt-transport-https  && sudo apt update && sudo apt install code -y && \
    code --install-extension ms-iot.vscode-ros && \
#    code --install-extension ms-vscode.cpptools && \
#    code --install-extension ms-vscode.cpptools-extension-pack && \ 
    code --install-extension ms-python.python 
USER ros
RUN bash -c 'mkdir ~/Desktop && \
    ln -s /usr/share/applications/code.desktop ~/Desktop/code.desktop && \
    ln -s /usr/share/applications/terminator.desktop ~/Desktop/terminator.desktop && \
    mkdir -p /home/ros/rap'


