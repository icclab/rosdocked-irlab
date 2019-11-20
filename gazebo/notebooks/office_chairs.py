#!/usr/bin/env python
# coding: utf-8

# In[ ]:

from matplotlib import pyplot as plt
from pcg_gazebo.simulation.properties import Mesh
from pcg_gazebo.simulation import create_object, SimulationModel
from pcg_gazebo.task_manager import Server, get_rostopic_list, get_rosservice_list
from pcg_gazebo.generators import WorldGenerator
import math
import random
import trimesh
import re
import os

# If there is a Gazebo instance running, you can spawn the box into the simulation
# First create a simulation server
server = Server()
# Create a simulation manager named default
server.create_simulation('default', ros_port=11311, gazebo_port=11345)
simulation = server.get_simulation('default')
# Run an instance of the empty.world scenario
# This is equivalent to run
#      roslaunch gazebo_ros empty_world.launch
# with all default parameters
simulation.create_gazebo_empty_world_task(gui=False, paused=True)
simulation.create_rqt_task()


# In[ ]:


# start a ROS node that can save images on service call
TASK_IMAGE_SAVE = dict(
    name='image save',
    command='rosrun image_view image_saver image:=/camera_standalone/camera/image_raw _save_all_image:=false',
    type=None,
    has_gazebo=False,
    params=dict(filename_format="image_%04d.jpg") # not working and not passed
)
simulation.init_task(**TASK_IMAGE_SAVE)


# In[ ]:


# A task named 'gazebo' the added to the tasks list
print(simulation.get_task_list())
# But it is still not running
print('Is Gazebo running: {}'.format(simulation.is_task_running('gazebo')))
# Run Gazebo
simulation.run_all_tasks()

# Create a Gazebo proxy
gazebo_proxy = simulation.get_gazebo_proxy()

# Use the generator to spawn the model to the Gazebo instance running at the moment
generator = WorldGenerator(gazebo_proxy=gazebo_proxy)


# In[ ]:


# Add camera sensor
camera_sensor = SimulationModel(name='camera_standalone')
camera_sensor.static = True

camera_sensor.add_camera_sensor(
    add_visual=True, 
    add_collision=True, 
    add_ros_plugin=True,
    visualize=True,
    mass=0.01,
    size=[0.1, 0.1, 0.1],
    link_shape='cuboid',
    link_name='camera_link',
    image_width=1280,
    image_height=960,
    update_rate=5)

#print(camera_sensor.to_sdf())

# Spawn camera standalone model
generator.spawn_model(
    model=camera_sensor, 
    robot_namespace='camera_standalone',
    pos=[0, 0, 0.3])



# In[ ]:


# list ROS topics
#print('List of ROS topics:')
#for topic in simulation.get_rostopic_list():
#    print(' - ' + topic)
# list ROS services
#print('List of ROS services:')
for service in get_rosservice_list():
#    print(' - ' + service)
    match = re.search("image_saver_.*/save", service)
    if ( match != None ):
       snap_svc_id = service 
print('Service id: ' + snap_svc_id)
f= open("images.csv","w+")

# In[ ]:


# start loop
log_line = 'image_file, x, y, z, roll, pitch, yaw'
print log_line
f.write(log_line + "\n")
for i in range(1,5001):
    # Place and office chair in the world
    model = SimulationModel.from_gazebo_model('office_chair')
    x = random.random() * 6 + 1
    y = (random.random() - 0.5) * x # make y proportional to x so we stay in picture
    pos = [x, y, 0]
    rot = [0, 0, (random.random() - 0.5) * 2 * math.pi]
    generator.spawn_model(
        model=model, 
        robot_namespace='office_chair',
        pos = pos,
        rot = rot,
        replace=True)
    # unpause the phyisic simulation
    gazebo_proxy.unpause()
    # Call the service to save a jpeg of what the camera is seeing
    snapshotCmd = 'rosservice call ' + snap_svc_id
    os.popen(snapshotCmd)    
    log_line = 'left' + '{:04d}'.format(i) + '.jpg, ' + ', '.join(map(str, pos)) + ", " + ', '.join(map(str, rot))
    print log_line
    f.write(log_line + "\n")
    # pause the phyisic simulation
    gazebo_proxy.pause()


# In[ ]:
f.close()

# End the simulation by killing the Gazebo task
simulation.kill_all_tasks()


# In[ ]:




