#!/usr/bin/env python3
import math

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import Spawn

class Turtle:

    def __init__(self, vx=0.8, theta=0, x=0, y=0, exists=False):
        global summoner
        if not exists:
            rospy.wait_for_service('/spawn')
            summoner(x, y, 0, f"turtle{count}")
        self.x = x
        self.y = y
        self.theta = theta

        self.vx = vx
        self.vy = 0

        self.pub = rospy.Publisher(f'/turtle{count}/cmd_vel', Twist, queue_size=10)
        self.vel = Twist()

        rospy.Subscriber(f'/turtle{count}/pose', Pose, self.pose_callback)
        self.rotate(theta)
        self.updatevelocity()

    def pose_callback(self, pose):
        self.x = pose.x
        self.y = pose.y
        self.theta = pose.theta

    def updatevelocity(self):

        if self.y > 8 or self.y < 3:
            summon(self.vx,  math.pi + self.theta, self.x, self.y)
            self.rotate(math.pi)

        elif self.x > 8 or self.x < 3:
            summon(self.vx, math.pi + self.theta, self.x, self.y)
            self.rotate(math.pi)

        self.vel.linear.y = self.vx
        self.vel.linear.z = 0
        self.vel.linear.x = 0

        self.vel.angular.x = 0
        self.vel.angular.y = 0
        self.vel.angular.z = 0

        self.pub.publish(self.vel)

    def rotate(self, angle):
        theta_initital = self.theta

        while deltatheta(theta_initital, self.theta) < angle:

            self.vel.linear.y = 0
            self.vel.linear.z = 0
            self.vel.linear.x = 0

            self.vel.angular.x = 0
            self.vel.angular.y = 0
            self.vel.angular.z = 1

            self.pub.publish(self.vel)


def summon(vx, vy, x, y):
    global turtles
    global count
    if count < 16:
        count += 1
        turtles.append(Turtle(vx, vy, x, y))


def deltatheta(theta1, theta2):

    if theta2 < 0:
        theta2 += 2 * math.pi
    if theta1 < 0:
        theta1 += 2 * math.pi

    if theta2 < theta1:
        theta2 += 2 * math.pi

    return theta2 - theta1


if __name__ == '__main__':

    try:
        rospy.init_node('bouncy', anonymous=False)
        summoner = rospy.ServiceProxy('/spawn', Spawn)
        count = 1
        turtles = [Turtle(exists=True)]
        while not rospy.is_shutdown():
            for i in turtles:
                i.updatevelocity()

    except rospy.ROSInterruptException:
        exit(0)
