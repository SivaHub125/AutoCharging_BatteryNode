cmake_minimum_required(VERSION 3.0.2)
project(battery_indicator)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  message_generation
)

add_message_files(
  FILES
  BatteryStatus.msg
  ErrorStatus.msg
)

generate_messages(
  DEPENDENCIES
  std_msgs
)

catkin_package(
  CATKIN_DEPENDS message_runtime roscpp rospy std_msgs
)

catkin_install_python(PROGRAMS src/battery_node.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

catkin_install_python(PROGRAMS src/auto_charging.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)