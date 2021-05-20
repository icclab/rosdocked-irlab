FROM nvidia/opengl:1.2-glvnd-runtime

ARG SOURCEFORGE=https://sourceforge.net/projects
ARG TURBOVNC_VERSION=2.1.2
ARG VIRTUALGL_VERSION=2.5.2
ARG LIBJPEG_VERSION=1.5.2
ARG WEBSOCKIFY_VERSION=0.8.0
ARG NOVNC_VERSION=1.0.0

ENV ROS_DISTRO=foxy
ENV DEBIAN_FRONTEND=noninteractive
ARG ROS_PKG=desktop
ENV ROS_ROOT=/opt/ros/${ROS_DISTRO}
ARG RTI_NC_LICENSE_ACCEPTED=yes

# change the locale from POSIX to UTF-8
#RUN locale-gen en_US en_US.UTF-8 && update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
#ENV LANG=en_US.UTF-8

# add the ROS deb repo to the apt sources list
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
		curl \
		wget \
		gnupg2 \
		lsb-release \
    && rm -rf /var/lib/apt/lists/*

RUN wget --no-check-certificate https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc && apt-key add ros.asc
RUN sh -c 'echo "deb [arch=$(dpkg --print-architecture)] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" > /etc/apt/sources.list.d/ros2-latest.list'

# install development packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
		build-essential \
		cmake \
		git \
		libbullet-dev \
		libpython3-dev \
		python3-colcon-common-extensions \
		python3-flake8 \
		python3-pip \
		python3-pytest-cov \
		python3-rosdep \
		python3-setuptools \
		python3-vcstool \
		python3-rosinstall-generator \
		libasio-dev \
		libtinyxml2-dev \
		libcunit1-dev \
    && rm -rf /var/lib/apt/lists/*


# https://answers.ros.org/question/325245/minimal-ros2-installation/?answer=325249#post-id-325249
RUN mkdir -p ${ROS_ROOT}/src && \
    cd ${ROS_ROOT} && \
   rosinstall_generator --deps --rosdistro ${ROS_DISTRO} ${ROS_PKG} launch_xml launch_yaml example_interfaces > ros2.${ROS_DISTRO}.${ROS_PKG}.rosinstall && \
    cat ros2.${ROS_DISTRO}.${ROS_PKG}.rosinstall && \
    vcs import src < ros2.${ROS_DISTRO}.${ROS_PKG}.rosinstall

    
# install dependencies using rosdep
RUN apt-get update && \
    cd ${ROS_ROOT} && \
    rosdep init && \
    rosdep update && \
   # rosdep install --from-paths src --ignore-src --rosdistro ${ROS_DISTRO} -y --skip-keys "console_bridge fastcdr fastrtps rti-connext-dds-5.3.1 urdfdom_headers qt_gui" && \
    rosdep install --from-paths src --ignore-src --rosdistro ${ROS_DISTRO} -y --skip-keys "" 
#&& \
#    rm -rf /var/lib/apt/lists/*

# build it!
RUN cd ${ROS_ROOT} && colcon build --symlink-install


RUN echo 'source ${ROS_ROOT}/install/setup.bash' >> /root/.bashrc


# install turbovnc, virtualgl, noVNC
RUN cd /tmp && \
    curl -fsSL -O ${SOURCEFORGE}/turbovnc/files/${TURBOVNC_VERSION}/turbovnc_${TURBOVNC_VERSION}_amd64.deb \
        -O ${SOURCEFORGE}/libjpeg-turbo/files/${LIBJPEG_VERSION}/libjpeg-turbo-official_${LIBJPEG_VERSION}_amd64.deb \
        -O ${SOURCEFORGE}/virtualgl/files/${VIRTUALGL_VERSION}/virtualgl_${VIRTUALGL_VERSION}_amd64.deb \
        -O ${SOURCEFORGE}/virtualgl/files/${VIRTUALGL_VERSION}/virtualgl32_${VIRTUALGL_VERSION}_amd64.deb && \
    dpkg -i *.deb && \
    rm -f /tmp/*.deb && \
    sed -i 's/$host:/unix:/g' /opt/TurboVNC/bin/vncserver

ENV PATH ${PATH}:/opt/VirtualGL/bin:/opt/TurboVNC/bin


RUN curl -fsSL https://github.com/novnc/noVNC/archive/v${NOVNC_VERSION}.tar.gz | tar -xzf - -C /opt && \
    curl -fsSL https://github.com/novnc/websockify/archive/v${WEBSOCKIFY_VERSION}.tar.gz | tar -xzf - -C /opt && \
    mv /opt/noVNC-${NOVNC_VERSION} /opt/noVNC && \
    chmod -R a+w /opt/noVNC && \
    mv /opt/websockify-${WEBSOCKIFY_VERSION} /opt/websockify && \
    cd /opt/websockify && make && \
    cd /opt/noVNC/utils && \
    ln -s /opt/websockify

COPY xorg.conf /etc/X11/xorg.conf
COPY index.html /opt/noVNC/index.html

EXPOSE 40001
ENV DISPLAY :1

ARG USER=ros

# add ros user to container and make sudoer
RUN useradd -m -s /bin/bash -G video,plugdev ${USER} && \
echo "${USER} ALL=(ALL) NOPASSWD: ALL" > "/etc/sudoers.d/${USER}" && \
chmod 0440 "/etc/sudoers.d/${USER}"

RUN echo "export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libjemalloc.so.2:libdlfaker.so:libvglfaker.so" >> ~/.bashrc

# Defeat screen locking and power management
#RUN sudo mv /etc/xdg/autostart/lxqt-xscreensaver-autostart.desktop /etc/xdg/autostart/lxqt-xscreensaver-autostart.desktop_bak && \
#    sudo mv /etc/xdg/autostart/lxqt-powermanagement.desktop /etc/xdg/autostart/lxqt-powermanagement.desktop_bak && \
#    sudo mv /etc/xdg/autostart/upg-notifier-autostart.desktop /etc/xdg/autostart/upg-notifier-autostart.desktop_bak

# install git and other needed libs including catkin build
RUN apt update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends git apt-utils curl wget vim less  lsof net-tools git htop \
    libxrender1 lubuntu-desktop xvfb xterm terminator zenity mesa-utils \
    x11-xkb-utils xauth 
RUN apt-get install -y --no-install-recommends python ros-foxy-rviz2 ros-foxy-rviz2 ros-foxy-rqt-image-view libconsole-bridge-dev ros-foxy-gazebo-ros-pkgs ros-foxy-ros-core ros-foxy-geometry2


# add user to video group
RUN adduser ${USER} video
RUN adduser ${USER} plugdev

# Switch to user
USER "${USER}"


# Switch to the workspace
WORKDIR /home/${USER}


# Install desktop file for this user
RUN mkdir -p /home/${USER}/Desktop
COPY ./terminator.desktop /home/${USER}/Desktop/
RUN sudo chown ${USER}:${USER} /home/${USER}/Desktop/terminator.desktop
RUN mkdir -p /home/${USER}/.config/terminator
COPY ./terminator_config /home/${USER}/.config/terminator/config
COPY ./self.pem /home/${USER}/self.pem
RUN sudo chown ${USER}:${USER} /home/${USER}/self.pem
# Precede bash on all new terminator shells with vglrun so that 3d graphics apps will use the GPU
RUN sudo perl -pi -e 's/^Exec=terminator$/Exec=terminator -e "vglrun bash"/g' /usr/share/applications/terminator.desktop

# setup the X session started by turbovnc
RUN mkdir -p /home/${USER}/.vnc
COPY ./xstartup.turbovnc /home/${USER}/.vnc/xstartup.turbovnc
RUN sudo chown ${USER}:${USER} /home/${USER}/.vnc/xstartup.turbovnc

COPY start_desktop.sh /usr/local/bin/start_desktop.sh
CMD /usr/local/bin/start_desktop.sh



