#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list
import time
import math
import tf
from geometry_msgs.msg import Point

class MoveGroup (object):

    def __init__(self):
        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node("move_group_python")
        self.robot = moveit_commander.RobotCommander()
        scene = moveit_commander.PlanningSceneInterface()
        group_name = "panda_arm"
        self.group = moveit_commander.MoveGroupCommander(group_name)
        self.display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory, queue_size=20)
        
        # Create a subscriber that listens to the /nesne/merkez topic
        rospy.Subscriber('/nesne/merkezs', Point, self.callback)
        
    def callback(self, data):
    
        print(data.x)
        print(data.y)
    	
        dx = ((320-data.x))
        dy = ((239-data.y))
        
        dxx = (-1*0.001*(dy))
        dyy = (-1*0.001*(dx))
        
        print(dxx)
        print(dyy)
        self.numx = dxx
        self.numy = dyy
        self.numz = 0.0

    def go_to_pose_goal(self, numx, numy, numz):
        current_pose = self.group.get_current_pose().pose
        # Set the orientation of the gripper to point downward
        # You can use any desired orientation, for example:
        # roll = 0, pitch = math.pi, yaw = 0
        # will make the gripper look straight downward
        #roll = 0
        #pitch = math.pi
        #yaw = 0
        #q = tf.transformations.quaternion_from_euler(roll, pitch, yaw)
        #pose_goal.orientation.x = q[0]
        #pose_goal.orientation.y = q[1]
        #pose_goal.orientation.z = q[2]
        #pose_goal.orientation.w = q[3]
    
        # Set the position of the gripper
        current_pose.position.x += numx
        current_pose.position.y += numy
        current_pose.position.z += numz
    
        # Set the pose goal for the group
        self.group.set_pose_target(current_pose)

        # Plan and execute the motion
        plan = self.group.go(wait=True)
        self.group.stop()
        self.group.clear_pose_targets()
        
        
def main():
    tutorial = MoveGroup()
    while not rospy.is_shutdown():
        data = rospy.wait_for_message("/nesne/merkezs", Point)
        tutorial.callback(data)
        if tutorial.numx == 0 and tutorial.numy == 0:
           break
        tutorial.go_to_pose_goal(tutorial.numx, tutorial.numy, tutorial.numz)

if __name__ == "__main__":
    main()

    


   

