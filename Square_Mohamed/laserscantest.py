#!/usr/bin/env python
import rospy
from math import pi
from std_msgs.msg import Bool
from sensor_msgs.msg import LaserScan
View=pi/4
angle=View/2
def callback(data):
	pub = rospy.Publisher('wallcheck', Bool, queue_size=10)
	increment=data.angle_increment
	total_range=[]
	total_range.extend(data.ranges[int((2*pi-angle)/increment):int(2*pi/increment)])
	total_range.extend(data.ranges[0:int(angle/increment)])
	total_range.sort()
	#rospy.loginfo(total_range)
	if total_range[0]<0.5:
		rospy.loginfo("too close")
		pub.publish(True)
	else:
		pub.publish(False)

def listener():
	rospy.init_node('scanner', anonymous=True)
	rospy.Subscriber('/scan', LaserScan, callback)
	rospy.spin()

if __name__ == '__main__':
	listener()
