#!/usr/bin/env python3
#-*- coding:utf-8 -*-


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
from PySide2.QtWidgets import QApplication, QLineEdit, QLabel, QVBoxLayout, QWidget, QPushButton

class MoveGroup (object):

    def __init__(self):
        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node("move_group_python")
        self.robot = moveit_commander.RobotCommander()
        scene = moveit_commander.PlanningSceneInterface()
        group_name = "panda_arm"
        self.group = moveit_commander.MoveGroupCommander(group_name)
        self.display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory, queue_size=20)

    def go_to_pose_goal(self, numx, numy, numz):
        pose_goal = geometry_msgs.msg.Pose()
        # Set the orientation of the gripper to point downward
        # You can use any desired orientation, for example:
        # roll = 0, pitch = math.pi, yaw = 0
        # will make the gripper look straight downward
        roll = 0
        pitch = math.pi
        yaw = 0
        q = tf.transformations.quaternion_from_euler(roll, pitch, yaw)
        pose_goal.orientation.x = q[0]
        pose_goal.orientation.y = q[1]
        pose_goal.orientation.z = q[2]
        pose_goal.orientation.w = q[3]
        current_pose = self.group.get_current_pose().pose
        print("Gripper'ın şu anki x konumu: ", current_pose.position.x)
        print("Gripper'ın şu anki y konumu: ", current_pose.position.y)
        print("Gripper'ın şu anki z konumu: ", current_pose.position.z)
         
       

        # Set the position of the gripper
        pose_goal.position.x = numx
        pose_goal.position.y = numy
        pose_goal.position.z = numz

        # Set the pose goal for the group
        self.group.set_pose_target(pose_goal)

        # Plan and execute the motion
        plan = self.group.go(wait=True)
        self.group.stop()
        self.group.clear_pose_targets()

def on_send_clicked():
    numx = float(x_edit.text())
    numy = float(y_edit.text())
    numz = float(z_edit.text())
    tutorial.go_to_pose_goal(numx, numy, numz)
    
x_edit = None
y_edit = None
z_edit = None

def get_pose_goal():
    global x_edit, y_edit, z_edit
    app = QApplication([])
    window = QWidget()
    layout = QVBoxLayout()

    
    # Create a label and a line edit for the x value
    x_label = QLabel("x değeri:")
    x_edit = QLineEdit()
    layout.addWidget(x_label)
    layout.addWidget(x_edit)

    # Create a label and a line edit for the y value
    y_label = QLabel("y değeri:")
    y_edit = QLineEdit()
    layout.addWidget(y_label)
    layout.addWidget(y_edit)

    # Create a label and a line edit for the z value
    z_label = QLabel("z değeri:")
    z_edit = QLineEdit()
    layout.addWidget(z_label)
    layout.addWidget(z_edit)

    # Add the button to the layout
    send_button = QPushButton("Gönder")
    layout.addWidget(send_button)

    # Connect the button's clicked signal to the on_send_clicked slot
    send_button.clicked.connect(on_send_clicked)

    # Set the layout for the window and show it
    window.setLayout(layout)
    window.show()

    # Keep the GUI running until the user closes it
    sys.exit(app.exec_())

if __name__ == "__main__":
    tutorial = MoveGroup()
    get_pose_goal()

