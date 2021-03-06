#!/usr/bin/env python
import roslib
roslib.load_manifest('ErkanS')
import speech_recognition as sr
import rospy
from move_base_msgs.msg import MoveBaseGoal, MoveBaseAction
import actionlib
from geometry_msgs.msg import Twist

POS1_CMD = "go to position 1"
POS2_CMD = "go to position 2"
MOVE_CMD = "move"
LEFT_CMD = "left"
RIGHT_CMD = "right"
SHARP_LEFT_CMD = "sharp left"
SHARP_RIGHT_CMD = "sharp right"
STOP_CMD = "stop"
BACK_CMD = "back"
GOOD_BOY = "good boy"
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

pub = rospy.Publisher("mobile_base/commands/velocity", Twist, queue_size=10)

def twist(t):
    pub.publish(t)

def goal(g):
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()
    client.send(g)

def main():
    rospy.init_node('speech')


    word = ''
    while True:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
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
            t.linear.x = 0.5
	    for i in range(5):
                twist(t)
		rospy.sleep(0.5)
        elif word == SHARP_LEFT_CMD:
            t = Twist()
            t.angular.z = 4
            twist(t)
        elif word == SHARP_RIGHT_CMD:
            t = Twist()
            t.angular.z = -4
            twist(t)
        elif word == POS1_CMD:
            goal(POS1)
        elif word == POS2_CMD:
            goal(POS2)
	elif word == BACK_CMD:
	    t= Twist()
	    t.angular.z = 4
	    twist(t)
	    rospy.sleep(1)
	    twist(t)
	elif word == STOP_CMD:
	    t = Twist()
	    twist(t)
	elif word == LEFT_CMD:
	    t = Twist()
            t.angular.z = 2
            twist(t)
	elif word == RIGHT_CMD:
            t = Twist()
            t.angular.z = -2
            twist(t)
	elif word == GOOD_BOY:
	    t = Twist()
            t.angular.z = 3
	    for i in range(5):
                twist(t)
		rospy.sleep(0.5)  

	print(word == LEFT_CMD)


if __name__=="__main__":
    main()
