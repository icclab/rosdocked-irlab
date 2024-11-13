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
    
allAvailableResources_summit_init = {
    'battery_percent': read_from_sensor()
 #   'battery_percent': read_from_sensor('HDD Usage (SXLS0_180227AA)')[0],
 #   'battery_charging': read_from_sensor('HDD Usage (SXLS0_180227AA)')[1],
}

possibleLaunchfiles_summit_init = ['startmapping', 'bringup', 'savemap', 'savebag', 'stopbag']
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
        # Read the bag file as binary
        with open(bag_file_path, 'rb') as file:
            bag_data = file.read()

        # Convert the MCAP binary data to a string ??? How???
        bag_string = base64.b64encode(bag_data).decode('utf-8')

        return bag_string

    except FileNotFoundError:
        print("Error: Bagfile not found.")
        return None

async def triggerBringup_summit_handler(params):
    params = params['input'] if params['input'] else {}

    # Default values
    launchfileId = 'startmapping'

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
    savebagaction = None
    stopbagaction = None
    #process_bagrecording = None
    

    #if launchfileId == 'bringup' and batterypercent is None :
    if launchfileId == 'bringup':
        # If battery percentage is None, start the summit launch file
        print("Battery status unknown, start summit_bringup!")
        process_bringup = subprocess.Popen(['ros2', 'launch', 'icclab_summit_xl', 'summit_xl_real.launch.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Allow some time for the launch file to start
        time.sleep(20)  


        # Check if the process is still running
        if process_bringup.poll() is None:
            print("Launch file started successfully.")
            bringupaction = True
        else:
            print("Failed to start the launch file.")
            bringupaction = False

   # if launchfileId == 'startmapping' and batterypercent >= 30:
    if launchfileId == 'startmapping':
        # If battery percentage is more than 50, allow to start the mapping launch file
        print("Battery sufficient, start summit mapping!")
        #process_mapping = subprocess.Popen(['ros2', 'launch', 'slam_toolbox', 'online_async_launch.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process_mapping = subprocess.Popen(['ros2', 'launch', 'summit_xl_navigation', 'nav2_bringup_launch.py', 'use_sim_time:=false', 'slam:=True'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(20) 



        if process_mapping.poll() is None:
            print("Mapping started successfully.")
            mappingaction = True
        else:
            print("Failed to start mapping.")
            mappingaction = False

    if launchfileId == 'savemap': #and mappingaction == True:
        print("Mapping finished, save the map!")
        process_savemapping = subprocess.Popen(['ros2', 'launch', 'icclab_summit_xl', 'map_save.launch.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(20) 
       
        print("Map saved successfully.")
        saveaction = True
        
    if launchfileId == 'savebag':
        print("Starting recording rosbag!")
        global process_bagrecording
        process_bagrecording = subprocess.Popen(['exec ros2 bag record -s mcap -o my_bag -d 20 -b 50000000 -a'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
        time.sleep(20) 
       
        print("Bag recording started.")
        savebagaction = True
    
    if launchfileId == 'stopbag':
        print("Stopping recording rosbag!")
        if process_bagrecording.poll() is None:
            process_bagrecording.terminate()
            process_bagrecording.wait()
            time.sleep(20)
        #print(process_bagrecording)
        #process_bagrecording.terminate()#kill()
        #os.killpg(process_bagrecording, signal.SIGTERM)
        print("Bag recording stopped.")
        stopbagaction = True

            
        


       # if process_savemapping.poll() is None:
       #     print("Map saved successfully.")
       #     saveaction = True
       # else:
       #     print("Failed to save map.")
       #     saveaction = False
    

    # Read the current level of allAvailableResources_summit
    resources = await exposed_thing.read_property('allAvailableResources_summit')

    # Calculate the new level of resources
    newResources = resources.copy()
    newResources['battery_percent'] = read_from_sensor()
   # newResources['battery_charging'] = read_from_sensor('HDD Usage (SXLS0_180227AA)')[1]
    
    # Check if the amount of available resources is sufficient to launch
    if newResources['battery_percent'] <= 30:
        # Emit outOfResource event
        exposed_thing.emit_event('outOfResource', 'Low level of Battery Percentage')
        return {'result': False, 'message': 'battery is not sufficient'}
    
    # Now store the new level of allAvailableResources_summit 
    await exposed_thing.properties['allAvailableResources_summit'].write(newResources)

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
    
async def mapExport_summit_handler(params):
    params = params['input'] if params['input'] else {}
    map_file_path = '/home/ros/my_map.pgm'
    map_string = get_map_as_string(map_file_path)
    return map_string

async def bagExport_summit_handler(params):
    params = params['input'] if params['input'] else {}
    bag_file_path = '/home/ros/my_bag/my_bag_0.mcap'
    bag_string = get_rosbag_as_string(bag_file_path)
    return bag_string
    
async def allAvailableResources_read_summit_handler():
    allAvailableResources_summit_current = {
    'battery_percent': read_from_sensor()
 #   'battery_percent': read_from_sensor('HDD Usage (SXLS0_180227AA)')[0],
 #   'battery_charging': read_from_sensor('HDD Usage (SXLS0_180227AA)')[1],
    }

    return allAvailableResources_summit_current

async def currentValues_summit_handler(params):
    return {
        'result': True,
        'message': {
    'battery_percent': read_from_sensor()
 #   'battery_percent': read_from_sensor('HDD Usage (SXLS0_180227AA)')[0],
 #   'battery_charging': read_from_sensor('HDD Usage (SXLS0_180227AA)')[1],
        }
    }


