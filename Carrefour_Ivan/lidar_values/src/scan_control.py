#! /usr/bin/env python

import rospy
import numpy as np
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist
from math import atan2

min_dist_right = 10.0
min_dist_left = 10.0
min_dist = 10.0
dist = []

def callback(msg):
    global min_dist
    global min_dist_right
    min_dist_right = 10.0
    global min_dist_left
    min_dist_left = 10.0
    global dist_right
    global dist_left

    dist_right = msg.ranges[0:20]
    dist_left = msg.ranges[340:360]

    for i in dist_right:
	if i == 0.0:
		pass
	elif i < min_dist_right:
		min_dist_right = i
	else:
		pass

    for i in dist_left:
	if i == 0.0:
		pass
	elif i < min_dist_left:
		min_dist_left = i
	else:
		pass
    
    print("Right min distance {}".format(min_dist_right))
    print("Left min distance {}".format(min_dist_left))
    min_dist = min(min_dist_right, min_dist_left)
    print("Min distance {}".format(min_dist))
	

rospy.init_node('scan_values', "speed_controller")
sub = rospy.Subscriber('/scan', LaserScan, callback)
#rospy.spin()

x = 0.0
y = 0.0 
theta = 0.0

print("passing")
 
def newOdom(msg):
    global x
    global y
    global theta
 
    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y
 
    rot_q = msg.pose.pose.orientation
    (roll, pitch, theta) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])
 
#rospy.init_node("speed_controller")
 
sub = rospy.Subscriber("/odometry/filtered", Odometry, newOdom)
pub = rospy.Publisher("/cmd_vel", Twist, queue_size = 10)
 
speed = Twist()
 
r = rospy.Rate(40)

while not rospy.is_shutdown():
 
#    if min_dist < 1.75:
#        speed.linear.x = 0.0
#        speed.angular.z = 0.3
    if min_dist_left < 1.0 and min_dist == min_dist_left:
        if speed.angular.z <= 0.0:
            speed.linear.x = 0.0
            speed.angular.z = -0.3
    elif min_dist_right < 1.0 and min_dist == min_dist_right:
        if speed.angular.z >= 0.0:
            speed.linear.x = 0.0
            speed.angular.z = 0.3
    else:
        speed.linear.x = 0.5
        speed.angular.z = 0.0

    pub.publish(speed)
    r.sleep() 
