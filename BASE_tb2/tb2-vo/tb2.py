import logging
import rclpy
from rclpy.node import Node

from std_msgs.msg import Bool
from std_msgs.msg import Float32
from diagnostic_msgs.msg import DiagnosticArray

import subprocess
import time
import base64 
import os
import signal
#from mcap.mcap_reader import McapReader

logging.basicConfig()
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def read_from_sensor(sensorType):
    if sensorType != 'kobuki: Battery':
        print(f"Sensor type '{sensorType}' is not supported.")
        return None
    
    battery_percent = None 
    battery_charging = None

    class BatteryRead(Node):
        def __init__(self):
            super().__init__('battery_read')
            self.subscription = self.create_subscription(DiagnosticArray, '/diagnostics', self.diagnostics_callback, 10)

        def diagnostics_callback(self, msg):
            nonlocal battery_percent
            nonlocal battery_charging
            for status in msg.status:
                if status.name == 'kobuki: Battery':
                    for item in status.values:
                        if item.key == 'Percent':
                            battery_percent = float(item.value)
                            # print(f'battery percent is {self.battery_level}%')
                        if item.key == 'Charging State':
                            if item.value == 'Trickle Charging' or 'Full Charging':
                                battery_charging = True
                            elif item.value == 'Not Charging':
                                battery_charging = False

    def main():
        rclpy.init()
        battery_read = BatteryRead()
        rclpy.spin_once(battery_read, timeout_sec=1.0)
        # rclpy.spin(battery_read)
        battery_read.destroy_node()
        rclpy.shutdown()

    main()

    return battery_percent, battery_charging
    
allAvailableResources_init = {
    'battery_percent': read_from_sensor('kobuki: Battery')[0],
    'battery_charging': read_from_sensor('kobuki: Battery')[1],
}

possibleLaunchfiles_init = ['startmapping', 'bringup', 'savemap']
mapdataExportTF_init = [True, False]

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

def get_rosbag_as_string(bag_file_path):
    try:
        with open(bag_file_path, 'rb') as file:
            binary_content = file.read()
            bag_string = base64.b64encode(binary_content).decode('utf-8')
        return bag_string

    except FileNotFoundError:
        print("Error: Bagfile not found.")
        return None


async def triggerBringup_handler(params):
    params = params['input'] if params['input'] else {}

    # Default values
    launchfileId = 'startmapping'

    # Check if params are provided
    launchfileId = params.get('launchfileId', launchfileId)

    # Check if there is resources
    battery_info = read_from_sensor('kobuki: Battery')
    batterypercent = battery_info[0] if battery_info is not None else None
    batterycharging = battery_info[1] if battery_info is not None else None
    print(f'Battery Percentage: {batterypercent}%')
    print(f'Battery is charging: {batterycharging}')
    bringupaction = None
    mappingaction = None
    saveaction = None
    savebagaction = None
    stopbagaction = None
   # process_bagrecording = None

    if launchfileId == 'bringup' and batterypercent is None :
        # If battery percentage is None, start the tb2 launch file
        print("Battery status unknown, start turtlebot2_bringup!")
        process_bringup = subprocess.Popen(['ros2', 'launch', 'turtlebot2_bringup', 'tb2_complete_no_map.launch.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Allow some time for the launch file to start
        time.sleep(15)  

        # Check if the process is still running
        if process_bringup.poll() is None:
            print("Launch file started successfully.")
            bringupaction = True
        else:
            print("Failed to start the launch file.")
            bringupaction = False

    if launchfileId == 'startmapping' and batterypercent >= 30:
        # If battery percentage is more than 50, allow to start the mapping launch file
        print("Battery sufficient, start turtlebot2 mapping!")
        process_mapping = subprocess.Popen(['ros2', 'launch', 'slam_toolbox', 'online_async_launch.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(10) 

        if process_mapping.poll() is None:
            print("Mapping started successfully.")
            mappingaction = True
        else:
            print("Failed to start mapping.")
            mappingaction = False

    if launchfileId == 'savemap': #and mappingaction == True:
        print("Mapping finished, save the map!")
        process_savemapping = subprocess.Popen(['ros2', 'launch', 'turtlebot2_bringup', 'map_save.launch.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(10) 

        print("Map saved successfully.")
        saveaction = True
   
    if launchfileId == 'savebag':
        print("Starting recording rosbag!")
        global process_bagrecording 
        #process_bagrecording = subprocess.Popen(['exec ros2 bag record -a -s mcap -o my_bag'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
        process_bagrecording = subprocess.Popen(['exec ros2 bag record -s mcap -o my_bag -d 20 -b 50000000 -a'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)

        time.sleep(1)
        print("Bag recording started.")
        savebagaction = True

# if process_savemapping.poll() is None:
       #     print("Map saved successfully.")
       #     saveaction = True
       # else:
       #     print("Failed to save map.")
       #     saveaction = False
    
    if launchfileId == 'stopbag':
        print("Stopping recording rosbag!")
        if process_bagrecording.poll() is None:
            process_bagrecording.terminate()    
            process_bagrecording.wait()
            time.sleep(1)
        print("Bag recording stopped.")
        stopbagaction = True

    # Read the current level of allAvailableResources
    resources = await exposed_thing.read_property('allAvailableResources')

    # Calculate the new level of resources
    newResources = resources.copy()
    newResources['battery_percent'] = read_from_sensor('kobuki: Battery')[0]
    newResources['battery_charging'] = read_from_sensor('kobuki: Battery')[1]
    
    # Check if the amount of available resources is sufficient to launch
    if newResources['battery_percent'] <= 30:
        # Emit outOfResource event
        exposed_thing.emit_event('outOfResource', 'Low level of Battery Percentage')
        return {'result': False, 'message': 'battery is not sufficient'}
    
    # Now store the new level of allAvailableResources 
    await exposed_thing.properties['allAvailableResources'].write(newResources)

    # Finally deliver the launchfile
    if launchfileId == 'bringup':
        return {'result': bringupaction, 'message': f'Your {launchfileId} is in progress!'}
    elif launchfileId == 'startmapping':
        return {'result': mappingaction, 'message': f'Your {launchfileId} is in progress!'}
    elif launchfileId == 'savemap':
        return {'result': saveaction, 'message': f'Your {launchfileId} is in progress!'}
    elif launchfileId == 'savebag':
        return {'result': savebagaction, 'message': f'Your {launchfileId} is in progress!'}
    elif launchfileId == 'stopbag':
        return {'result': stopbagaction, 'message': f'Your {launchfileId} is in progress!'}

async def mapExport_handler(params):
    params = params['input'] if params['input'] else {}


    map_file_path = '/home/ros/my_map.pgm'
    map_string = get_map_as_string(map_file_path)
    return map_string
#    if map_string is None
       # return {'result': mapExport, 'message': f'No map found on device!'}
#    else
#        return map_string
    

async def bagExport_handler(params):
    params = params['input'] if params['input'] else {}
    bag_file_path = '/home/ros/my_bag/my_bag_0.mcap'
    bag_string = get_rosbag_as_string(bag_file_path)
    return bag_string

async def allAvailableResources_read_handler():
    allAvailableResources_current = {
        'battery_percent': read_from_sensor('kobuki: Battery')[0],
        'battery_charging': read_from_sensor('kobuki: Battery')[1],
    }

    return allAvailableResources_current

async def currentValues_handler(params):
    return {
        'result': True,
        'message': {
            "battery_percent": read_from_sensor('kobuki: Battery')[0],
            "battery_charging": read_from_sensor('kobuki: Battery')[1]
        }
    }



