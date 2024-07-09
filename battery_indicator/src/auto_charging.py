
import rospy
import yaml
from battery_indicator.msg import BatteryStatus
from battery_indicator.msg import ErrorStatus



class BatteryMonitor:
    def __init__(self):
        yaml_file="/home/myubuntu/ros-training/src/battery_indicator/config/param_battery.yaml"
        with open(yaml_file, 'r') as f:
            config = yaml.safe_load(f)
        self.battery_percentage = 100.0
        self.critical_percent = rospy.get_param('~critical_percent', 5)
        self.full_battery = rospy.get_param('~full_battery', 100)
        self.warning_percentage = rospy.get_param('~warning_percentage', 20)
        self.publisher = rospy.Publisher('battery_status', BatteryStatus, queue_size=10)
        self.error_publisher=rospy.Publisher('error_status',ErrorStatus,queue_size=10)
        self.timer_unplug = rospy.Timer(rospy.Duration(0.2), self.update_battery_unplugged)
        self.timer_plug = None
        self.error_msg = False
        rate=rospy.Rate(10)
        while not rospy.is_shutdown():
            self.Status()
            rate.sleep()
    
    def Status(self):
        if (self.battery_percentage < self.critical_percent):
            while(self.battery_percentage < self.full_battery):
                self.handle_plug_cable(True)
            self.handle_plug_cable(False)
        if (self.battery_percentage < self.warning_percentage):
            self.error_msg=True
        else:
            rospy.loginfo("Battery Sufficient")

    def handle_plug_cable(self, req):
        if req and self.timer_plug is None:
            self.timer_plug = rospy.Timer(rospy.Duration(0.2), self.update_battery_plugged)
            self.timer_unplug.shutdown()
            self.timer_unplug = None
            rospy.loginfo("Charging started")
        elif not req and self.timer_plug is not None:
            self.timer_plug.shutdown()
            self.timer_plug = None
            self.timer_unplug = rospy.Timer(rospy.Duration(0.2), self.update_battery_unplugged)
            rospy.loginfo("Charging stopped")

    def update_battery_plugged(self, event):
        if self.battery_percentage < 100:
            self.battery_percentage += 1
        self.publish_status()
        self.publish_errorstatus()

    def update_battery_unplugged(self, event):
        if self.battery_percentage > 0:
            self.battery_percentage -= 1
        self.publish_status()
        self.publish_errorstatus()

    def publish_errorstatus(self):
        msg=ErrorStatus()
        msg.error=self.error_msg
        msg.description = "Robot is about to deplete its battery, don't assign new job."
        if(msg.error): 
            self.error_publisher.publish(msg)
        self.error_msg=False

    def publish_status(self):
        msg = BatteryStatus()
        msg.batteryPercentage = self.battery_percentage
        self.publisher.publish(msg)
    
if __name__ == '__main__':
    rospy.init_node('battery_monitor')
    bm = BatteryMonitor()
    rospy.spin()
