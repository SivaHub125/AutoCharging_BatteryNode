import rospy
from battery_indicator.msg import BatteryStatus
from std_srvs.srv import SetBool, SetBoolResponse

class BatteryMonitor:
    def __init__(self):
        self.battery_percentage = 100.0
        self.publisher = rospy.Publisher('battery_status', BatteryStatus, queue_size=10)
        self.service = rospy.Service('/plug_cable', SetBool, self.handle_plug_cable)
        self.timer_unplug = rospy.Timer(rospy.Duration(0.2), self.update_battery_unplugged)
        self.timer_plug = None

    def handle_plug_cable(self, req):
        if req.data and self.timer_plug is None:
            self.timer_plug = rospy.Timer(rospy.Duration(0.1), self.update_battery_plugged)
            self.timer_unplug.shutdown()
            self.timer_unplug = None
            return SetBoolResponse(True, "Charging started")
        elif not req.data and self.timer_plug is not None:
            self.timer_plug.shutdown()
            self.timer_plug = None
            self.timer_unplug = rospy.Timer(rospy.Duration(0.2), self.update_battery_unplugged)
            return SetBoolResponse(True, "Charging stopped")
        return SetBoolResponse(False, "No state change required")

    def update_battery_plugged(self, event):
        if self.battery_percentage < 100:
            self.battery_percentage += 1
        self.publish_status()

    def update_battery_unplugged(self, event):
        if self.battery_percentage > 0:
            self.battery_percentage -= 1
        self.publish_status()

    def publish_status(self):
        msg = BatteryStatus()
        msg.batteryPercentage = self.battery_percentage
        self.publisher.publish(msg)

if __name__ == '__main__':
    rospy.init_node('battery_monitor')
    bm = BatteryMonitor()
    rospy.spin()
