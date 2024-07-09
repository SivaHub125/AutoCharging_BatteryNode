# **Battery Node**

## Basic Setup

1. Create a catkin workspace along with src folder
2. Add this [folder](https://github.com/SivaHub125/AutoCharging_BatteryNode) inside src folder
3. Build: `catkin_make`
   - `source ./devel/setup.bash`

## _Manual Battery Node_ [link](https://github.com/SivaHub125/AutoCharging_BatteryNode/blob/main/battery_indicator/src/battery_node.py)

#### RUN
- Terminal 1 : `roslaunch battery_indicator battery_indicator.launch`
- Terminal 2 : `rostopic list` then `rostopic echo /battery_status` 

## _AutoCharging Battery Node_ [link](https://github.com/SivaHub125/AutoCharging_BatteryNode/blob/main/battery_indicator/src/auto_charging.py)

#### RUN
- Terminal 1 : `roslaunch battery_indicator auto_indicator.launch`
- Terminal 2 : `rostopic list` then `rostopic echo /battery_status`
- Terminal 3 : `rostopic echo /error_status`

#### Troubleshoot
Error: `RLException: [auto_indicator.launch] is neither a launch file in package [battery_indicator] nor is [battery_indicator] a launch file name
The traceback for the exception was written to the log file`

* Source all the terminals to avoid this error
* `source ./devel/setup.bash`
