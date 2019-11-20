#!/usr/bin/env python

import rospy
from std_msgs.msg import Bool
from geometry_msgs.msg import Twist
def move(data):
	pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
	twist=Twist()
	if data.data==True:
		twist.linear.x=0
		twist.angular.z=0.5
	else:
		twist.linear.x =0.5
		twist.angular.z=0
	pub.publish(twist)

def listener():
	rospy.init_node('listening', anonymous=True)
	rospy.Subscriber('wallcheck', Bool, move)
	rospy.spin()

if __name__ == '__main__':
	listener()
