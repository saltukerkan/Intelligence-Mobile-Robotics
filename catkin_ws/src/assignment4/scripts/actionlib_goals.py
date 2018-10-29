#!/usr/bin/env python

import roslib
roslib.load_manifest('ErkanS')
import rospy
from geometry_msgs.msg import PoseStamped , Pose #, Header, Point, Quaternion
from nav_msgs.msg import Odometry
import time
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib_msgs.msg import GoalStatusArray

def callback(data):
    if data.status_list.pop().status == 3:
        print('success')

def main():
    global goals, pub, goal
    goals = []
    rospy.init_node('go_to_goal')

    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()

    #pub = rospy.Publisher("/move_base_simple/goal", PoseStamped, queue_size=1)
    
    p1 = MoveBaseGoal()
    p1.target_pose.header.frame_id = 'map'
    p1.target_pose.pose.position.x = -10
    p1.target_pose.pose.position.y = 3
    p1.target_pose.pose.position.z = -0.00143
    p1.target_pose.pose.orientation.z = -0.00413

    #p1.header.frame_id = "saltuk_map"
    #p1.pose.orientation.x = 0
    #p1.pose.orientation.y = 0
    #goal = p1
    #pub.publish(goal)

   
    client.send_goal(p1)
    client.wait_for_result()#rospy.Duration.from_sec(5.0))
    #rospy.Subscriber("/move_base/status", GoalStatusArray, callback, queue_size=1)
    #rospy.spin()

    p2 = MoveBaseGoal()
    p2.target_pose.header.frame_id = 'map'
    p2.target_pose.pose.position.x = 3.58
    p2.target_pose.pose.position.y = 3.45
    p2.target_pose.pose.position.z = -0.00143
    p2.target_pose.pose.orientation.z = -0.00413

    client.send_goal(p2)
    client.wait_for_result()#rospy.Duration.from_sec(5.0))

    p3 = MoveBaseGoal()
    p3.target_pose.header.frame_id = 'map'
    p3.target_pose.pose.position.x = -0.8
    p3.target_pose.pose.position.y = -2.3
    p3.target_pose.pose.position.z = -0.00143
    p3.target_pose.pose.orientation.z = -0.00413

    client.send_goal(p3)
    client.wait_for_result()#rospy.Duration.from_sec(5.0))

    p4 = MoveBaseGoal()
    p4.target_pose.header.frame_id = 'map'
    p4.target_pose.pose.position.x = -0.8
    p4.target_pose.pose.position.y = -6.5
    p4.target_pose.pose.position.z = -0.00143
    p4.target_pose.pose.orientation.z = -0.00413


    client.send_goal(p4)
    client.wait_for_result()#rospy.Duration.from_sec(5.0))


#    p2 = PoseStamped()
#    p2.pose.position.x = 0
#    p2.pose.position.y = 0
#    goals.append(p2)

#    p3 = PoseStamped()
#    p3.pose.position.x = 0
#    p3.pose.position.y = 0
#    goals.append(p3)

#    p4 = PoseStamped()
#    p4.pose.position.x = 0
#    p4.pose.position.y = 0
#    goals.append(p4)


#    rate = rospy.Rate(10)

    rospy.spin()

if __name__=="__main__":
    main()
