#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np
   
def callback(data):
    global rotate_prev
    speed = 0.2
    rotate = 0.01
    try:
        cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
        print(e)

    gray_image = cv2.cvtColor(cv_image[cv_image.shape[0]-30:cv_image.shape[0]], cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray_image, (5,5), 0)
    thresh = cv2.threshold(blur, 80, 255, cv2.THRESH_BINARY_INV)[1]
    #contours = cv2.findContours(thresh, 1, cv2.CHAIN_APPROX_NONE)


    M = cv2.moments(thresh)
    if len(thresh) > 0:
    	M = cv2.moments(thresh)
    	if M["m00"] != 0:
    		cX = int(M["m10"] / M["m00"])
    		speed = 0.2
    		rotate = -(cX - cv_image.shape[1]*0.5) / 150
    		print(cX, cv_image.shape, rotate * 150)

	else:
	    rotate = rotate_prev * 2
	    speed = 0.1

    print(rotate_prev)

    move.angular.z = rotate
    move.linear.x = speed - 0.05 * rotate

    rotate_prev = rotate    

    pub.publish(move)

rotate = 0.001
rotate_prev = 0.001
speed = 0.2


bridge = CvBridge()
move = Twist()

rospy.init_node('topic_publisher')
try:
	sub = rospy.Subscriber('/rrbot/camera1/image_raw', Image, callback)
except CvBridgeError as e:
    print(e)

pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
rate = rospy.Rate(2)

rospy.spin()