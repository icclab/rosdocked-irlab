import logging
import rclpy
from rclpy.node import Node

from std_msgs.msg import Bool
from std_msgs.msg import Float32
from sensor_msgs.msg import NavSatFix
from visualization_msgs.msg import Marker
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

import yaml

process_startfrontcamera = None
process_startarmcamera = None
process_startliquidpicking = None
process_startsensordeploy = None
process_startpeopledetect = None
process_startliquidpickingmarker = None


def load_map_origin(yaml_file_path):
    """
    Loads a ROS map YAML file and returns the origin coordinates.

    Args:
        yaml_file_path (str): Path to the YAML file.

    Returns:
        tuple: (x, y, yaw) origin coordinates as floats.
    """
    with open(yaml_file_path, 'r') as file:
        map_data = yaml.safe_load(file)
        origin = map_data.get('origin', [0.0, 0.0, 0.0])
        x, y, yaw = origin
        return x, y, yaw



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


def read_liquid_marker():
    
    x_liquid = None 
    y_liquid = None 

    class MarkerRead(Node):
        def __init__(self):
            super().__init__('marker_read')
            self.marker_subscription = self.create_subscription(Marker,'/summit/leakage_marker',self.marker_callback,10)

        def marker_callback(self, msg: Marker):
            nonlocal x_liquid
            nonlocal y_liquid
            x_liquid = msg.pose.position.x
            y_liquid =  msg.pose.position.y
            self.get_logger().info(f"Marker: {x_liquid}, {y_liquid}")


    def main():
        rclpy.init()
        marker_read = MarkerRead()
        rclpy.spin_once(marker_read, timeout_sec=1.0)
        marker_read.destroy_node()
        rclpy.shutdown()

    main()

    return x_liquid, y_liquid

def read_person_marker():
    
    x_person = None 
    y_person = None 

    class PersonMarkerRead(Node):
        def __init__(self):
            super().__init__('marker_person_read')
            self.marker_person_subscription = self.create_subscription(Marker,'/summit/person_marker',self.person_marker_callback,10)

        def person_marker_callback(self, msg: Marker):
            nonlocal x_person
            nonlocal y_person
            x_person = msg.pose.position.x
            y_person = msg.pose.position.y
            self.get_logger().info(f"Marker: {x_person}, {y_person}")


    def main():
        rclpy.init()
        person_marker_read = PersonMarkerRead()
        rclpy.spin_once(person_marker_read, timeout_sec=1.0)
        person_marker_read.destroy_node()
        rclpy.shutdown()

    main()

    return x_person, y_person

# Initialize Resources
altitude, latitude, longitude = read_from_gps_sensor()
x_liquid, y_liquid =  read_liquid_marker()
x_person, y_person =  read_person_marker()

allAvailableResources_init = {
    'altitude': altitude,
    'latitude': latitude,
    'longitude': longitude,
    'battery_percent': read_from_sensor(),
    'deployed_sensors': 0,
    'liquid_samples': 0,
    'x_liquid': x_liquid,
    'y_liquid': y_liquid,
    'x_person': x_person,
    'y_person': y_person 
}

possibleLaunchfiles_summit_init = ['startmapping_summit', 'start3dmapping_summit', 'bringup_summit', 'savemap_summit', 'startarmcamera_summit', 'stoparmcamera_summit', 'startfrontcamera_summit', 'stopfrontcamera_summit']
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
    mapping3daction = None
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
        time.sleep(5)  


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
        time.sleep(5) 


        if process_mapping.poll() is None:
            print("Mapping started successfully.")
            mappingaction = True
        else:
            print("Failed to start mapping.")
            mappingaction = False
           
    if launchfileId == 'start3dmapping_summit':
        process_3dmapping = subprocess.Popen(['ros2', 'launch', 'icclab_summit_xl', 'rtabmap.launch.py', 'use_sim_time:=false'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(5) 

        if process_3dmapping.poll() is None:
            print("3D Mapping started successfully.")
            mapping3daction = True
        else:
            print("Failed to start 3D mapping.")
            mapping3daction = False

    if launchfileId == 'savemap_summit': #and mappingaction == True:
        print("Mapping finished, save the map!")
        process_savemapping = subprocess.Popen(['ros2', 'launch', 'icclab_summit_xl', 'map_save.launch.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(5) 
       
        print("Map saved successfully.")
        saveaction = True
    
    
    if launchfileId == 'startarmcam_summit':
        #process_startarmcamera = subprocess.Popen(['ros2', 'launch', 'icclab_summit_xl', 'oak.camera.launch.py', 'namespace:=summit'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process_startarmcamera = subprocess.Popen(['ros2', 'launch', 'person_detect', 'person_detect.launch.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(5) 


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
        time.sleep(5) 

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

    if launchfileId == 'liquid_sampling_from_marker':
        global process_startliquidpickingmarker

        coordinates = read_liquid_marker()
        
        global count_liquid_samples 
        count_liquid_samples += len(coordinates)
            # Ensure coordinates are in the correct format
        print(f"Coordinates: {coordinates}")  
        if not coordinates:
            return {'result': False, 'message': 'No coordinates provided from marker.'}


        # Create the coordinates string without quotes around numbers
        coordinates_str = json.dumps(coordinates)  # This will produce '[ [0.5, 0] ]'

        coordinates_str = coordinates_str.replace('[', '[[')  
        coordinates_str = coordinates_str.replace(']', ']]')        
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
        if process_startliquidpickingmarker:
            if process_startliquidpickingmarker.poll() is None:
                print("Terminating gracefully existing process...")
                try:
                    # Gracefully terminate the process
                    process_startliquidpickingmarker.send_signal(signal.SIGINT)
                    process_startliquidpickingmarker.wait(timeout=10)
                    print("Process terminated gracefully.")
                            # **Start a new subprocess and keep track of it**
                    try:
                        print("Starting new process...")
                        process_startliquidpickingmarker = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
                    process_startliquidpickingmarker.kill()
                    process_startliquidpickingmarker.wait()
                    try:
                        print("Starting new process...")
                        process_startliquidpickingmarker = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
                    process_startliquidpickingmarker = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
                process_startliquidpickingmarker = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                return {
                    'result': True,
                    'message': f'Liquid sampling started at coordinates: {coordinates_str}!'
                }
            except Exception as e:
                print(f"Failed to start process: {e}")
                return {'result': False, 'message': 'Failed to start process.'}   



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
    elif launchfileId == 'start3dmapping_summit':
        return {'result': mapping3daction, 'message': f'Your {launchfileId} is in progress!'}
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


  

async def people_detect_summit_handler(params):
        global process_startpeopledetect

        params = params.get('input', {}) or {}
        

        # Launch the ROS2 command
        command = [
            "bash", "-c",
            f"ros2 launch person_detection person_detect.launch.py"
        ]

            # **Terminate existing process if running**
        if process_startpeopledetect:
            if process_startpeopledetect.poll() is None:
                print("Terminating gracefully existing process...")
                try:
                    # Gracefully terminate the process
                    process_startpeopledetect.send_signal(signal.SIGINT)
                    process_startpeopledetect.wait(timeout=10)
                    print("Process terminated gracefully.")
                            # **Start a new subprocess and keep track of it**
                    try:
                        print("Starting new process...")
                        process_startpeopledetect = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        return {
                            'result': True,
                            'message': f'People detection started!'
                        }
                    except subprocess.CalledProcessError as e:
                        print(f"Failed to start process: {e}")
                        return {'result': False, 'message': 'Failed to start process.'}    
                except subprocess.TimeoutExpired:
                    # Forcefully kill the process if it didn't terminate
                    print("Process did not terminate in time. Killing it forcefully.")
                    process_startpeopledetect.kill()
                    process_startpeopledetect.wait()
                    try:
                        print("Starting new process...")
                        process_startpeopledetect = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        return {
                            'result': True,
                            'message': f'People detection started!'
                        }
                    except subprocess.CalledProcessError as e:
                        print(f"Failed to start process: {e}")
                        return {'result': False, 'message': 'Failed to start process.'} 
                except Exception as e:
                    print(f"An error occurred: {e}")
            else:
                try:
                    print("Starting new process...")
                    process_startpeopledetect = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    return {
                        'result': True,
                        'message': f'People detection started!'
                    }
                except Exception as e:
                    print(f"Failed to start process: {e}")
                    return {'result': False, 'message': 'Failed to start process.'}   
        else:
            try:
                print("Starting new process...")
                process_startpeopledetect = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                return {
                    'result': True,
                    'message': f'People detected started!'
                }
            except Exception as e:
                print(f"Failed to start process: {e}")
                return {'result': False, 'message': 'Failed to start process.'}       
 
async def mapExport_summit_handler(params):
    params = params['input'] if params['input'] else {}
    map_file_path = '/home/ros/my_map.pgm'
    map_string = get_map_as_string(map_file_path)
    return map_string

async def mapOriginExport_summit_handler(params):
    params = params['input'] if params['input'] else {}
    map_metadata_file_path = '/home/ros/my_map.yaml'
    x, y, yaw = load_map_origin("/home/ros/my_map.yaml")
    mapOrigin = {
    'x': x,
    'y': y,
    'yaw': yaw
    }
    print(f"Origin coordinates: x={x}, y={y}, yaw={yaw}")
    return mapOrigin
    
        
async def allAvailableResources_summit_read_handler():
    altitude, latitude, longitude = read_from_gps_sensor()
    x_liquid, y_liquid =  read_liquid_marker()
    x_person, y_person =  read_person_marker()
    allAvailableResources_current = {
    'altitude': altitude,
    'latitude': latitude,
    'longitude': longitude,
    'battery_percent': read_from_sensor(),
    'deployed_sensors': count_deployed_sensors,
    'liquid_samples': count_liquid_samples,
    'x_liquid': x_liquid,
    'y_liquid': y_liquid,
    'x_person': x_person,
    'y_person': y_person 
 #   'battery_percent': read_from_sensor('HDD Usage (SXLS0_180227AA)')[0],
 #   'battery_charging': read_from_sensor('HDD Usage (SXLS0_180227AA)')[1],
    }

    return allAvailableResources_current

async def currentValues_summit_handler(params):
    altitude, latitude, longitude = read_from_gps_sensor()
    x_liquid, y_liquid =  read_liquid_marker()
    x_person, y_person =  read_person_marker()
    return {
        'result': True,
        'message': {
    'altitude': altitude,
    'latitude': latitude,
    'longitude': longitude,
    'battery_percent': read_from_sensor(),
    'deployed_sensors': count_deployed_sensors,
    'liquid_samples': count_liquid_samples,
    'x_liquid': x_liquid,
    'y_liquid': y_liquid,
    'x_person': x_person,
    'y_person': y_person 
 #   'battery_percent': read_from_sensor('HDD Usage (SXLS0_180227AA)')[0],
 #   'battery_charging': read_from_sensor('HDD Usage (SXLS0_180227AA)')[1],
        }
    }


