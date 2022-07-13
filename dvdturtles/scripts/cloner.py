#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import Spawn


class Turtle:

    def __init__(self, vx=1, vy=1.1, x=0, y=0, exists=False):
        global summoner
        if not exists:
            rospy.wait_for_service('/spawn')
            summoner(x, y, 0, f"turtle{count}")
        self.x = x
        self.y = y

        self.vx = vx
        self.vy = vy

        self.pub = rospy.Publisher(f'/turtle{count}/cmd_vel', Twist, queue_size=10)
        self.vel = Twist()

        rospy.Subscriber(f'/turtle{count}/pose', Pose, self.pose_callback)
        self.updatevelocity()

    def pose_callback(self, pose):
        self.x = pose.x
        self.y = pose.y

    def updatevelocity(self):

        if self.y > 10 and self.vy > 0:
            summon(-self.vx, -self.vy, self.x, self.y)
            self.vy = -self.vy

        elif self.y < 1 and self.vy < 0:
            summon(-self.vx, -self.vy, self.x, self.y)
            self.vy = -self.vy

        elif self.x > 10 and self.vx > 0:
            summon(-self.vx, -self.vy, self.x, self.y)
            self.vx = -self.vx

        elif self.x < 1 and self.vx < 0:
            summon(-self.vx, -self.vy, self.x, self.y)
            self.vx = -self.vx

        self.vel.linear.x = self.vx
        self.vel.linear.y = self.vy
        self.vel.linear.z = 0

        self.vel.angular.x = 0
        self.vel.angular.y = 0
        self.vel.angular.z = 0

        self.pub.publish(self.vel)


def summon(vx, vy, x, y):
    global turtles
    global count
    if count < 16:
        count += 1
        turtles.append(Turtle(vx, vy, x, y))


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
