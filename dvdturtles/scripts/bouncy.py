import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from time import sleep
import sys
import math
import subprocess

x1, y1, t1 = 0, 0, 0


def pose_callback1(pose):
    global x1, y1, t1
    x1 = pose.x
    y1 = pose.y
    t1 = pose.theta


def move_turtles():
    global x1, y1, t1

    vx = 0.8
    vy = 0.6

    rospy.init_node('bouncy', anonymous=False)
    pub1 = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rospy.Subscriber('/turtle1/pose', Pose, pose_callback1)

    rate = rospy.Rate(60)  # 60hz
    vel1 = Twist()

    while not rospy.is_shutdown():

        if y1 > 8 and vy > 0:
            vy = -vy
        if y1 < 3 and vy < 0:
            vy = -vy
        if x1 > 8 and vx > 0:
            vx = -vx
        if x1 < 3 and vx < 0:
            vx = -vx

        vel1.linear.x = vx
        vel1.linear.y = vy
        vel1.linear.z = 0

        vel1.angular.x = 0
        vel1.angular.y = 0
        vel1.angular.z = 0
        pub1.publish(vel1)

        rate.sleep()


if __name__ == '__main__':

    try:
        move_turtles()
    except rospy.ROSInterruptException:
        pass
