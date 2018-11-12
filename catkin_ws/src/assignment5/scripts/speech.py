#!/usr/bin/env python
import roslib
roslib.load_manifest('ErkanS')
import speech_recognition as sr
import rospy
from actionlib_msgs.msg import MoveBaseGoal, MoveBaseAction
import actionlib_msgs
from geometry_msgs.msg import Twist

POS1_CMD = "go to position 1"
POS2_CMD = "go to position 2"
MOVE_CMD = "move"
LEFT_CMD = "left"
RIGHT_CMD = "right"
STOP_CMD = "stop"
POS1 = MoveBaseGoal()
POS1.target_pose.header.frame_id = 'map'
POS1.target_pose.pose.position.x = -10
POS1.target_pose.pose.position.y = 3
POS1.target_pose.pose.position.z = -0.00143
POS1.target_pose.pose.orientation.z = -0.00413
POS2 = MoveBaseGoal()
POS2.target_pose.header.frame_id = 'map'
POS2.target_pose.pose.position.x = -0.8
POS2.target_pose.pose.position.y = -6.5
POS2.target_pose.pose.position.z = -0.00143
POS2.target_pose.pose.orientation.z = -0.00413

def twist(t):
    pub = rospy.Publisher("mobile_base/commands/velocity", Twist, queue_size=10)
    pub.publish(t)

def goal(g):
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()
    client.send(g)

def main():
    rospy.init_node('speech')


    while True:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
        word = ''
        try:
            word =  r.recognize_google(audio)
        except sr.UnknownValueError:
            print("Duzgun konus anlasilmiyo")
        except sr.RequestError as e:
            print("error abi")
            print(e)

        print(repr(word))
        if word == MOVE_CMD:
            t = Twist()
            t.linear.x = 1
            twist(t)
        elif word == LEFT_CMD:
            t = Twist()
            t.angular.z = 1.56
            twist(t)
        elif word == RIGHT_CMD:
            t = Twist()
            t.angular.z = -1.56
            twist(t)
        elif word == POS1_CMD:
            goal(POS1)
        elif word == POS2_CMD:
            goal(POS2)
        # elif word == STOP_CMD:
        #     t = Twist()
        #     t.linear.x = 0
        #     t.linear.y = 0
        #     t.linear.z = 0
        #     t.angular.x = 0
        #     t.angular.y = 0
        #     t.angular.z = 0
        #     twist(t)


if __name__=="__main__":
    main()
