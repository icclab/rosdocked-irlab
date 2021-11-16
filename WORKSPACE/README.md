# Noetic Containers With included Workspace

## On your own laptop (Any OS supporting docker compose)

When working with your own laptop, you can launch the containers using docker-compose with the following command:

    docker-compose -f docker-compose-cpu.yml up

This will launch two containers, one with the ROS Kinetic environment installed for you to work on, and one for novnc (the GUI) which you can access through your browser at: 
[http://localhost/vnc.html](http://localhost/vnc.html) 

In another terminal, you can access the ROS container with:

    docker exec -it rosdocked bash
  
From that console you can launch the scripts you want (e.g., roslaunch ...).
In the end you'll have a split environment where you have anything that has to do with the GUI in the browser, but you can launch commands from the console.

*NOTE:* VPN clients can  get in the way of the networking between the containers. If you experience issues try disconnecting from the VPN and restarting the composition.

### Windows users

You'll need a TTY application, so:
- find out the ID of the ros container in the composition with *docker ps*
- launch bash in that container with:

        winpty docker exec -it YOUR_CONTAINER_ID bash

You can use that command multiple times to get multiple consoles.

-------------
## On your own laptop (Linux with Xserver and docker)

You may also want to start a container without novnc, but connecting to a *local running Xserver instance*. For this you can use the following command:

    ./run_cpu.sh

Note that the xhost needs to be correctly set in order to make it work correctly. (xhost+ would do the trick)
