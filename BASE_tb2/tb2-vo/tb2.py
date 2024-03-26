import logging
import rclpy
from rclpy.node import Node

from std_msgs.msg import Bool
from std_msgs.msg import Float32
from diagnostic_msgs.msg import DiagnosticArray

import subprocess
import time

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
            self.subscription = self.create_subscription(DiagnosticArray, '/diagnostics', self.diagnostics_callback, 20)
#            self.battery_percent_pub = self.create_publisher(Float32, '/battery_level', 10)
#            self.battery_charging_pub = self.create_publisher(Bool, '/battery_charging', 10)

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
                            if item.value == 'Trickle Charging':
                                battery_charging = True
                            elif item.value == 'Not Charging':
                                battery_charging = False

         #   if battery_percent is not None:
         #       msg_percentage = Float32()
         #       msg_percentage.data = battery_percent
         #       self.battery_percent_pub.publish(msg_percentage)
         #   if battery_charging is not None:
         #       msg_charging = Bool()
         #       msg_charging.data = battery_charging
         #       self.battery_charging_pub.publish(msg_charging)

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
    else:
        print(f'Battery Percentage: {batterypercent}%')

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
    #else:
   #     print("Unable to start mapping")
   #     mappingaction = False

    if launchfileId == 'savemap': #and mappingaction == True:
        print("Mapping finished, save the map!")
        process_mapping = subprocess.Popen(['ros2', 'launch', 'turtlebot2_bringup', 'map_save.launch.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(10) 

        if process_mapping.poll() is None:
            print("Map saved successfully.")
            saveaction = True
        else:
            print("Failed to save map.")
            saveaction = False
    

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
            "battery_status": read_from_sensor('kobuki: Battery')[1]
        }
    }

