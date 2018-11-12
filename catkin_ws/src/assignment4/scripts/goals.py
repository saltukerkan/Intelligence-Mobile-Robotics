#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import PoseStamped , Pose #, Header, Point, Quaternion
from nav_msgs.msg import Odometry

def callback(data):
    global goals, pub
    var = 10
    x_reached = False
    y_reached = False
    if data.pose.pose.position.x + var > goal.position.x and data.pose.pose.position.x - var < goal.position.x:
        # next goal
        x_reached = True
    if data.pose.pose.position.y + var > goal.position.y and
    data.pose.pose.position.y - var < goal.position.y:
        y_reached = True
    if x_reached and y_reached:
        pub.publish(goals.pop(0))
        #next goal

def main():
    global goals, pub
    goals = []
    pub = rospy.Publisher("/move_base_simple/goal", PoseStamped, queue_size=10)
    rospy.init_node('go_to_goal')

    p1 = PoseStamped()
    p1.pose.position.x = 0
    p1.pose.position.y = 0
    pub.publish(p1)

    p2 = PoseStamped()
    p2.pose.position.x = 0
    p2.pose.position.y = 0
    goals.append(p2)

    p3 = PoseStamped()
    p3.pose.position.x = 0
    p3.pose.position.y = 0
    goals.append(p3)

    p4 = PoseStamped()
    p4.pose.position.x = 0
    p4.pose.position.y = 0
    goals.append(p4)

    rospy.Subscriber("/odom", Odometry, callback(data), queue_size=1)

    rate = rospy.Rate(10)

if __name__=="__main__":
    main()
