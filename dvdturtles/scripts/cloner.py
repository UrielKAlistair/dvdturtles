#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import Spawn

"""
- shifting to class for task
- setting up your ide properly
- git, trello
- pep 8
"""


class Ears:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.t1 = 0

    def pose_callback(self, pose):
        self.x = pose.x
        self.y = pose.y
        self.t1 = pose.theta


class Turtle:
    def __init__(self, vx=0.8, vy=0.6, x=0, y=0, exists=False):
        global summoner
        global count
        self.vx = vx
        self.vy = vy
        self.pub = rospy.Publisher(f'/turtle{count}/cmd_vel', Twist, queue_size=10)
        self.vel = Twist()
        self.myears = Ears(x, y)

        rospy.Subscriber(f'/turtle{count}/pose', Pose, self.myears.pose_callback)
        if not exists and count<16:
            count += 1
            rospy.wait_for_service('/spawn')
            summoner(x, y, 0, f"turtle{count}")


    def updatevelocity(self):

        if self.myears.y > 8 and self.vy > 0:
            summon(-self.vx, -self.vy, self.myears.x, self.myears.y)
            self.vy = -self.vy
        elif self.myears.y < 3 and self.vy < 0:
            summon(-self.vx, -self.vy, self.myears.x, self.myears.y)
            self.vy = -self.vy

        elif self.myears.x > 8 and self.vx > 0:
            summon(-self.vx, -self.vy, self.myears.x, self.myears.y)
            self.vx = -self.vx
        elif self.myears.x < 3 and self.vx < 0:
            summon(-self.vx, -self.vy, self.myears.x, self.myears.y)
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
    turtles.append(Turtle(vx, vy, x, y))


if __name__ == '__main__':

    try:
        rospy.init_node('bouncy', anonymous=False)
        summoner = rospy.ServiceProxy('/spawn', Spawn)
        count=1
        turtles = [Turtle(exists=True)]
        while not rospy.is_shutdown():
            for i in turtles:
                i.updatevelocity()

    except rospy.ROSInterruptException:
        exit(0)
