import logging
import rclpy
from rclpy.node import Node

from std_msgs.msg import Bool
from std_msgs.msg import Float32
from sensor_msgs.msg import NavSatFix
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


process_startfrontcamera = None
process_startarmcamera = None
process_startliquidpicking = None
process_startsensordeploy = None

def read_from_sensor():
    
    battery_percent = None 

    class BatteryRead(Node):
        def __init__(self):
            super().__init__('battery_read')
            self.subscription = self.create_subscription(Float32, '/summit/robotnik_base_hw/battery', self.battery_callback, 10)

        def battery_callback(self, msg):
            nonlocal battery_percent

    def main():
        rclpy.init()
        battery_read = BatteryRead()
        rclpy.spin_once(battery_read, timeout_sec=1.0)
        battery_read.destroy_node()
        rclpy.shutdown()

    main()

    return battery_percent

def read_from_gps_sensor():
    
    altitude = None 
    longitude = None 
    latitude = None 

    class GpsRead(Node):
        def __init__(self):
            super().__init__('gps_read')
            self.subscription = self.create_subscription(NavSatFix, '/summit/fix', self.gps_callback, 10)

        def gps_callback(self, msg):
            nonlocal altitude
            nonlocal latitude
            nonlocal longitude
            altitude = msg.altitude
            latitude = msg.latitude
            longitude = msg.longitude
            self.get_logger().info(f"GPS: {latitude}, {longitude}, {altitude}")


    def main():
        rclpy.init()
        gps_read = GpsRead()
        rclpy.spin_once(gps_read, timeout_sec=1.0)
        gps_read.destroy_node()
        rclpy.shutdown()

    main()

    return altitude, latitude, longitude

# Initialize Resources
altitude, latitude, longitude = read_from_gps_sensor()

allAvailableResources_init = {
    'altitude': altitude,
    'latitude': latitude,
    'longitude': longitude,
    'battery_percent': read_from_sensor(),
    'deployed_sensors': 0,
    'liquid_samples': 0
}

possibleLaunchfiles_summit_init = ['startmapping_summit', 'bringup_summit', 'savemap_summit', 'startarmcamera_summit', 'stoparmcamera_summit', 'startfrontcamera_summit', 'stopfrontcamera_summit']
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
    battery_info = read_from_sensor()
    batterypercent = battery_info if battery_info is not None else None
    print(f'Battery Percentage: {batterypercent}%')
    bringupaction = None
    mappingaction = None
    saveaction = None
    startarmcameraaction = None
    startfrontcameraaction = None
    stoparmcameraaction = None
    stopfrontcameraaction = None
    global process_startarmcamera  
    global process_startfrontcamera
    
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
    
    
    if launchfileId == 'startarmcam_summit':
        process_startarmcamera = subprocess.Popen(['ros2', 'launch', 'icclab_summit_xl', 'oak.camera.launch.py', 'namespace:=summit'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(10) 

        if process_startarmcamera.poll() is None:
            print("Arm camera started successfully.")
            startarmcameraaction = True
        else:
            print("Failed to start arm camera.")
            startarmcameraaction = False
   
    if launchfileId == 'stoparmcam_summit':
        if process_startarmcamera:
            # Ensure that the process exists and is running
            if process_startarmcamera.poll() is None:
                try:
                    # Gracefully terminate the process
                    process_startarmcamera.send_signal(signal.SIGINT)
                    process_startarmcamera.wait(timeout=30)
                    print("Process terminated gracefully.")
                except subprocess.TimeoutExpired:
                    # Forcefully kill the process if it didn't terminate
                    print("Process did not terminate in time. Killing it forcefully.")
                    process_startarmcamera.kill()
                    process_startarmcamera.wait()
                except Exception as e:
                    print(f"An error occurred: {e}")
                stoparmcameraaction = True
            print("Arm camera stopped.")
        else:
            print("No arm camera process running.")
            stoparmcameraaction = False
        process_startarmcamera = None  # Reset the process variable

    if launchfileId == 'startfrontcam_summit':
        process_startfrontcamera = subprocess.Popen(['ros2', 'launch', 'icclab_summit_xl', 'astra_mini.launch.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(10) 

        if process_startfrontcamera.poll() is None:
            print("Front camera started successfully.")
            startfrontcameraaction = True
        else:
            print("Failed to start front camera.")
            startfrontcameraaction = False
   
    if launchfileId == 'stopfrontcam_summit':
        if process_startfrontcamera:
            # Ensure that the process exists and is running
            if process_startfrontcamera.poll() is None:
                try:
                    # Gracefully terminate the process
                    process_startfrontcamera.send_signal(signal.SIGINT)
                    process_startfrontcamera.wait(timeout=30)
                    print("Process terminated gracefully.")
                except subprocess.TimeoutExpired:
                    # Forcefully kill the process if it didn't terminate
                    print("Process did not terminate in time. Killing it forcefully.")
                    process_startfrontcamera.kill()
                    process_startfrontcamera.wait()
                except Exception as e:
                    print(f"An error occurred: {e}")
                stopfrontcameraaction = True
            print("Front camera stopped.")
        else:
            print("No front camera process running.")
            stopfrontcameraaction = False
        process_startfrontcamera = None  # Reset the process variable

    # Read the current level of allAvailableResources_summit
    resources = await exposed_thing.read_property('allAvailableResources_summit')

    # Calculate the new level of resources
    newResources = resources.copy()
    newResources['battery_percent'] = read_from_sensor()
    
    # Check if the amount of available resources is sufficient to launch
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
    elif launchfileId == 'startarmcam_summit':
        return {'result': startarmcameraaction, 'message': f'Your {launchfileId} is in progress!'}
    elif launchfileId == 'stoparmcam_summit':
        return {'result': stoparmcameraaction, 'message': f'Your {launchfileId} is in progress!'}
    elif launchfileId == 'startfrontcam_summit':
        return {'result': startfrontcameraaction, 'message': f'Your {launchfileId} is in progress!'}
    elif launchfileId == 'stopfrontcam_summit':
        return {'result': stopfrontcameraaction, 'message': f'Your {launchfileId} is in progress!'}

    

async def sample_liquid_summit_handler(params):
        global process_startliquidpicking

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

        # Launch the ROS2 command
        command = [
            "bash", "-c",
            f"ros2 launch liquid_pickup liquid_pickup_launch_real.py coordinates:={coordinates_str}"
        ]
        print(f"Final command: {command}")

            # **Terminate existing process if running**
        if process_startliquidpicking:
            if process_startliquidpicking.poll() is None:
                print("Terminating gracefully existing process...")
                try:
                    # Gracefully terminate the process
                    process_startliquidpicking.send_signal(signal.SIGINT)
                    process_startliquidpicking.wait(timeout=10)
                    print("Process terminated gracefully.")
                            # **Start a new subprocess and keep track of it**
                    try:
                        print("Starting new process...")
                        process_startliquidpicking = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        return {
                            'result': True,
                            'message': f'Liquid sampling started at coordinates: {coordinates_str}!'
                        }
                    except subprocess.CalledProcessError as e:
                        print(f"Failed to start process: {e}")
                        return {'result': False, 'message': 'Failed to start process.'}    
                except subprocess.TimeoutExpired:
                    # Forcefully kill the process if it didn't terminate
                    print("Process did not terminate in time. Killing it forcefully.")
                    process_startliquidpicking.kill()
                    process_startliquidpicking.wait()
                    try:
                        print("Starting new process...")
                        process_startliquidpicking = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        return {
                            'result': True,
                            'message': f'Liquid sampling started at coordinates: {coordinates_str}!'
                        }
                    except subprocess.CalledProcessError as e:
                        print(f"Failed to start process: {e}")
                        return {'result': False, 'message': 'Failed to start process.'} 
                except Exception as e:
                    print(f"An error occurred: {e}")
            else:
                try:
                    print("Starting new process...")
                    process_startliquidpicking = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    return {
                        'result': True,
                        'message': f'Liquid sampling started at coordinates: {coordinates_str}!'
                    }
                except Exception as e:
                    print(f"Failed to start process: {e}")
                    return {'result': False, 'message': 'Failed to start process.'}   
        else:
            try:
                print("Starting new process...")
                process_startliquidpicking = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                return {
                    'result': True,
                    'message': f'Liquid sampling started at coordinates: {coordinates_str}!'
                }
            except Exception as e:
                print(f"Failed to start process: {e}")
                return {'result': False, 'message': 'Failed to start process.'}           



"""         # Execute the command in a subprocess
        try:
            subprocess.run(command, check=True)
            return {
            'result': True,
            'message': f'Liquid sampling completed at coordinates: {coordinates_str}!'
            }
        except subprocess.CalledProcessError as e:
            print(f"Command failed with return code {e.returncode}")
            print(f"Error message: {e}")
            return {'result': False, 'message': 'An undefined error occurred.'} """



async def deploy_sensor_summit_handler(params):
        global process_startsensordeploy
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

                # **Terminate existing process if running**
        if process_startsensordeploy:
            if process_startsensordeploy.poll() is None:
                print("Terminating gracefully existing process...")
                try:
                    # Gracefully terminate the process
                    process_startsensordeploy.send_signal(signal.SIGINT)
                    process_startsensordeploy.wait(timeout=10)
                    print("Process terminated gracefully.")
                            # **Start a new subprocess and keep track of it**
                    try:
                        process_startsensordeploy = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        return {
                            'result': True,
                            'message': f'Sensor deployment started at coordinates: {coordinates_str}!'
                        }
                    except Exception as e:
                        print(f"Failed to start process: {e}")
                        return {'result': False, 'message': 'Failed to start process.'}
                except subprocess.TimeoutExpired:
                    # Forcefully kill the process if it didn't terminate
                    print("Process did not terminate in time. Killing it forcefully.")
                    process_startsensordeploy.kill()
                    process_startsensordeploy.wait()
                    try:
                        process_startsensordeploy = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        return {
                            'result': True,
                            'message': f'Sensor deployment started at coordinates: {coordinates_str}!'
                        }
                    except Exception as e:
                        print(f"Failed to start process: {e}")
                        return {'result': False, 'message': 'Failed to start process.'}
                except Exception as e:
                    print(f"An error occurred: {e}")
            else:
                try:
                    print("Starting new process...")
                    process_startsensordeploy = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    return {
                        'result': True,
                        'message': f'Sensor deployment sampling started at coordinates: {coordinates_str}!'
                    }
                except Exception as e:
                    print(f"Failed to start process: {e}")
                    return {'result': False, 'message': 'Failed to start process.'}   
        else:
            try:
                print("Starting new process...")
                process_startsensordeploy = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                return {
                    'result': True,
                    'message': f'Sensor deployment started at coordinates: {coordinates_str}!'
                }
            except Exception as e:
                print(f"Failed to start process: {e}")
                return {'result': False, 'message': 'Failed to start process.'}   


"""         # Execute the command in a subprocess
        try:
            subprocess.run(command, check=True)
            return {
            'result': True,
            'message': f'Sensor deployment completed at coordinates: {coordinates_str}!'
            }
        except subprocess.CalledProcessError as e:
            print(f"Command failed with return code {e.returncode}")
            print(f"Error message: {e}")
            return {'result': False, 'message': 'An undefined error occurred.'} """

 
async def mapExport_summit_handler(params):
    params = params['input'] if params['input'] else {}
    map_file_path = '/home/ros/my_map.pgm'
    map_string = get_map_as_string(map_file_path)
    return map_string

    
async def allAvailableResources_summit_read_handler():
    altitude, latitude, longitude = read_from_gps_sensor()
    allAvailableResources_current = {
    'altitude': altitude,
    'latitude': latitude,
    'longitude': longitude,
    'battery_percent': read_from_sensor(),
    'deployed_sensors': count_deployed_sensors,
    'liquid_samples': count_liquid_samples
 #   'battery_percent': read_from_sensor('HDD Usage (SXLS0_180227AA)')[0],
 #   'battery_charging': read_from_sensor('HDD Usage (SXLS0_180227AA)')[1],
    }

    return allAvailableResources_current

async def currentValues_summit_handler(params):
    altitude, latitude, longitude = read_from_gps_sensor()
    return {
        'result': True,
        'message': {
    'altitude': altitude,
    'latitude': latitude,
    'longitude': longitude,
    'battery_percent': read_from_sensor(),
    'deployed_sensors': count_deployed_sensors,
    'liquid_samples': count_liquid_samples
 #   'battery_percent': read_from_sensor('HDD Usage (SXLS0_180227AA)')[0],
 #   'battery_charging': read_from_sensor('HDD Usage (SXLS0_180227AA)')[1],
        }
    }


