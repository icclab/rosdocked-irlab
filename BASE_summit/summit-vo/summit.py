import logging
import rclpy
from rclpy.node import Node

from std_msgs.msg import Bool
from std_msgs.msg import Float32
#from diagnostic_msgs.msg import DiagnosticArray

import subprocess
import time
import base64

logging.basicConfig()
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

import os
import signal

import asyncio
import json

def read_from_sensor():
#def read_from_sensor(sensorType):
   # if sensorType != 'HDD Usage (SXLS0_180227AA)':
        #print(f"Sensor type '{sensorType}' is not supported.")
        #return None
    
    battery_percent = None 
   # battery_charging = None

    class BatteryRead(Node):
        def __init__(self):
            super().__init__('battery_read')
            #self.subscription = self.create_subscription(DiagnosticArray, '/diagnostics', self.diagnostics_callback, 10)
            self.subscription = self.create_subscription(Float32, '/summit/robotnik_base_hw/battery', self.battery_callback, 10)

        def battery_callback(self, msg):
            nonlocal battery_percent
       #     nonlocal battery_charging
            battery_percent = msg.data
      #      for status in msg.status:
      #          if status.name == 'HDD Usage (SXLS0_180227AA)':
      #              for item in status.values:
      #                  if item.key == 'Update Status':
      #                      battery_percent = float(item.value)
      #                  if item.key == 'Disk Space Reading':
    #                      if item.value == 'OK':
    #                            battery_charging = True

    def main():
        rclpy.init()
        battery_read = BatteryRead()
        rclpy.spin_once(battery_read, timeout_sec=1.0)
        battery_read.destroy_node()
        rclpy.shutdown()

    main()

    return battery_percent#, battery_charging
    
allAvailableResources_init = {
    'battery_percent': read_from_sensor(),
    'deployed_sensors': 0,
    'liquid_samples': 0
 #   'battery_percent': read_from_sensor('HDD Usage (SXLS0_180227AA)')[0],
 #   'battery_charging': read_from_sensor('HDD Usage (SXLS0_180227AA)')[1],
}

possibleLaunchfiles_summit_init = ['startmapping_summit', 'bringup_summit', 'savemap_summit']
mapdataExportTF_init = [True, False]

count_deployed_sensors = 0
count_liquid_samples = 0

def get_map_as_string(map_file_path):
    try:
        # Read the PGM file as binary
        with open(map_file_path, 'rb') as file:
            pgm_data = file.read()

        # Convert the PGM binary data to a string
        pgm_string = base64.b64encode(pgm_data).decode('utf-8')

        return pgm_string

    except FileNotFoundError:
        print("Error: Map file not found.")
        return None


async def triggerBringup_summit_handler(params):
    params = params['input'] if params['input'] else {}

    # Default values
    launchfileId = 'startmapping_summit'

    # Check if params are provided
    launchfileId = params.get('launchfileId', launchfileId)

    # Check if there is resources
    #battery_info = read_from_sensor('HDD Usage (SXLS0_180227AA)')
    battery_info = read_from_sensor()
    #batterypercent = battery_info[0] if battery_info is not None else None
    batterypercent = battery_info if battery_info is not None else None
    #batterycharging = battery_info[1] if battery_info is not None else None
    print(f'Battery Percentage: {batterypercent}%')
    #print(f'Battery is charging: {batterycharging}')
    bringupaction = None
    mappingaction = None
    saveaction = None

    

    #if launchfileId == 'bringup' and batterypercent is None :
    if launchfileId == 'bringup_summit':
        # If battery percentage is None, start the summit launch file
        print("Battery status unknown, start summit_bringup!")
        process_bringup = subprocess.Popen(['ros2', 'launch', 'icclab_summit_xl', 'summit_xl_real.launch.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Allow some time for the launch file to start
        time.sleep(10)  


        # Check if the process is still running
        if process_bringup.poll() is None:
            print("Launch file started successfully.")
            bringupaction = True
        else:
            print("Failed to start the launch file.")
            bringupaction = False

   # if launchfileId == 'startmapping' and batterypercent >= 30:
    if launchfileId == 'startmapping_summit':
        # If battery percentage is more than 50, allow to start the mapping launch file
        print("Battery sufficient, start summit mapping!")
        #process_mapping = subprocess.Popen(['ros2', 'launch', 'slam_toolbox', 'online_async_launch.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
       # process_mapping = subprocess.Popen(['ros2', 'launch', 'summit_xl_navigation', 'nav2_bringup_launch.py', 'use_sim_time:=false', 'slam:=True'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process_mapping = subprocess.Popen(['ros2', 'launch', 'icclab_summit_xl', 'summit_xl_nav2.launch.py', 'use_sim_time:=false', 'slam:=True', 'params_file:=/home/ros/colcon_ws/install/icclab_summit_xl/share/icclab_summit_xl/config/nav2_params_real.yaml'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(10) 


        if process_mapping.poll() is None:
            print("Mapping started successfully.")
            mappingaction = True
        else:
            print("Failed to start mapping.")
            mappingaction = False

    if launchfileId == 'savemap_summit': #and mappingaction == True:
        print("Mapping finished, save the map!")
        process_savemapping = subprocess.Popen(['ros2', 'launch', 'icclab_summit_xl', 'map_save.launch.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(10) 
       
        print("Map saved successfully.")
        saveaction = True
   

    # Read the current level of allAvailableResources_summit
    resources = await exposed_thing.read_property('allAvailableResources_summit')

    # Calculate the new level of resources
    newResources = resources.copy()
    newResources['battery_percent'] = read_from_sensor()
   # newResources['battery_charging'] = read_from_sensor('HDD Usage (SXLS0_180227AA)')[1]
    
    # Check if the amount of available resources is sufficient to launch
    #Commenting for now as it gives an error with the return
    if newResources['battery_percent'] <= 30:
        # Emit outOfResource event
        exposed_thing.emit_event('outOfResource_summit', 'Low level of Battery Percentage')
        return {'result': False, 'message': 'battery is not sufficient'}
    
    # Now store the new level of allAvailableResources_summit 
    await exposed_thing.properties['allAvailableResources_summit'].write(newResources)

    # Finally deliver the launchfile
    if launchfileId == 'bringup_summit':
        print("Launch file return successfully.")
        return {'result': bringupaction, 'message': f'Your {launchfileId} is in progress!'}
    elif launchfileId == 'startmapping_summit':
        return {'result': mappingaction, 'message': f'Your {launchfileId} is in progress!'}
    elif launchfileId == 'savemap_summit':
        return {'result': saveaction, 'message': f'Your {launchfileId} is in progress!'}

    

async def sample_liquid_summit_handler(params):
        params = params.get('input', {}) or {}
        coordinates = params.get('coordinates')
        global count_liquid_samples 
        count_liquid_samples += len(coordinates)
            # Ensure coordinates are in the correct format
        print(f"Coordinates: {coordinates}")  
        if not coordinates:
            return {'result': False, 'message': 'No coordinates provided for sensor deployment.'}


        # Create the coordinates string without quotes around numbers
        coordinates_str = json.dumps(coordinates)  # This will produce '[ [0.5, 0] ]'
        
        # Replace quotes around numbers (by re-serializing to a string)
        coordinates_str = coordinates_str.replace('"', '')  # Remove quotes around numbers

        # Format the coordinates string for ROS 2 launch
        coordinates_str = f"'{coordinates_str}'"  # Wrap coordinates in single quotes for the ROS 2 command


         # Now manually construct the final string to match: '"[[1, 0]]"'
        coordinates_str = f"\"{coordinates_str}\""  # Wrap it with double quotes around the entire string
        print(f"Formatted coordinates for ROS 2 command: {coordinates_str}")

        # Source the ROS workspace and launch the ROS2 command
        command = [
            "bash", "-c",
            f"ros2 launch liquid_pickup liquid_pickup_launch_real.py coordinates:={coordinates_str}"
        ]
        print(f"Final command: {command}")

        # Execute the command in a subprocess
        try:
            subprocess.run(command, check=True)
            return {
            'result': True,
            'message': f'Liquid sampling completed at coordinates: {coordinates_str}!'
            }
        except subprocess.CalledProcessError as e:
            print(f"Command failed with return code {e.returncode}")
            print(f"Error message: {e}")
            return {'result': False, 'message': 'An undefined error occurred.'}



async def deploy_sensor_summit_handler(params):
        params = params.get('input', {}) or {}
        coordinates = params.get('coordinates')
        global count_deployed_sensors
        count_deployed_sensors += len(coordinates)
            # Ensure coordinates are in the correct format
        print(f"Coordinates: {coordinates}")  
        if not coordinates:
            return {'result': False, 'message': 'No coordinates provided for sensor deployment.'}


        # Create the coordinates string without quotes around numbers
        coordinates_str = json.dumps(coordinates)  # This will produce '[ [0.5, 0] ]'
        
        # Replace quotes around numbers (by re-serializing to a string)
        coordinates_str = coordinates_str.replace('"', '')  # Remove quotes around numbers

        # Format the coordinates string for ROS 2 launch
        coordinates_str = f"'{coordinates_str}'"  # Wrap coordinates in single quotes for the ROS 2 command


         # Now manually construct the final string to match: '"[[1, 0]]"'
        coordinates_str = f"\"{coordinates_str}\""  # Wrap it with double quotes around the entire string
        print(f"Formatted coordinates for ROS 2 command: {coordinates_str}")

        # Source the ROS workspace and launch the ROS2 command
        command = [
            "bash", "-c",
            f"ros2 launch liquid_pickup sensors_deploy_launch_real.py coordinates:={coordinates_str}"
        ]
        print(f"Final command: {command}")

        # Execute the command in a subprocess
        try:
            subprocess.run(command, check=True)
            return {
            'result': True,
            'message': f'Sensor deployment completed at coordinates: {coordinates_str}!'
            }
        except subprocess.CalledProcessError as e:
            print(f"Command failed with return code {e.returncode}")
            print(f"Error message: {e}")
            return {'result': False, 'message': 'An undefined error occurred.'}

 
async def mapExport_summit_handler(params):
    params = params['input'] if params['input'] else {}
    map_file_path = '/home/ros/my_map.pgm'
    map_string = get_map_as_string(map_file_path)
    return map_string

    
async def allAvailableResources_summit_read_handler():
    allAvailableResources_current = {
    'battery_percent': read_from_sensor(),
    'deployed_sensors': count_deployed_sensors,
    'liquid_samples': count_liquid_samples
 #   'battery_percent': read_from_sensor('HDD Usage (SXLS0_180227AA)')[0],
 #   'battery_charging': read_from_sensor('HDD Usage (SXLS0_180227AA)')[1],
    }

    return allAvailableResources_current

async def currentValues_summit_handler(params):
    return {
        'result': True,
        'message': {
    'battery_percent': read_from_sensor(),
    'deployed_sensors': count_deployed_sensors,
    'liquid_samples': count_liquid_samples
 #   'battery_percent': read_from_sensor('HDD Usage (SXLS0_180227AA)')[0],
 #   'battery_charging': read_from_sensor('HDD Usage (SXLS0_180227AA)')[1],
        }
    }


