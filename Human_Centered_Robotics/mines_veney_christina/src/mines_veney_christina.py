#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt
import numpy as np
import time

class TurtleBot:
    
    def __init__(self):
        # Creates a node with name 'turtlebot_controller' and make sure it is a
        # unique node (using anonymous=True).
        rospy.init_node('turtlebot_controller', anonymous=True)

        # Publisher which will publish to the topic '/turtle1/cmd_vel'.
        self.velocity_publisher = rospy.Publisher('/turtle1/cmd_vel',
                                                  Twist, queue_size=10)

        # A subscriber to the topic '/turtle1/pose'. self.update_pose is called
        # when a message of type Pose is received.
        self.pose_subscriber = rospy.Subscriber('/turtle1/pose',
                                                Pose, self.update_pose)

        self.pose = Pose()
        self.rate = rospy.Rate(10)
        
    def update_pose(self, data):
        """Callback function which is called when a new message of type Pose is
        received by the subscriber."""
        self.pose = data
        self.pose.x = round(self.pose.x, 4)
        self.pose.y = round(self.pose.y, 4)
        
    def euclidean_distance(self, goal_pose):
        """Euclidean distance between current pose and the goal."""
        return sqrt(pow((goal_pose.x - self.pose.x), 2) +
                    pow((goal_pose.y - self.pose.y), 2))
    
    def steering_angle(self, goal_pose):
        """See video: https://www.youtube.com/watch?v=Qh15Nol5htM."""
        return atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x)
    
    def angular_vel(self, goal_pose, constant=6.6):
        """See video: https://www.youtube.com/watch?v=Qh15Nol5htM."""
        return constant * (self.steering_angle(goal_pose) - self.pose.theta)
    
    def linear_vel(self, goal_pose, constant=1.2):
       """See video: https://www.youtube.com/watch?v=Qh15Nol5htM."""
       return constant * self.euclidean_distance(goal_pose)
    
    def move2goal(self, targetx, targety, decision):
        """Moves the turtle to the goal."""
        goal_pose = Pose()
        goal_pose.x = targetx
        goal_pose.y = targety

        distance_tolerance = 0.00008
        angle_tolerance = 0.0000005
        speed = 6.5
        vel_msg = Twist()
        self.rate.sleep()
        #print("current pos: " + str(self.pose.x) + " y " + str(self.pose.y))
        #print("target pos: " + str(targetx) + " y " + str(targety))
 
        if decision == 0: #go straight
            disx = abs(goal_pose.x - self.pose.x)
            disy = abs(goal_pose.y - self.pose.y)
            while disx > distance_tolerance or disy >distance_tolerance:
                disx = abs(goal_pose.x - self.pose.x)
                disy = abs(goal_pose.y - self.pose.y)
                if disx >= distance_tolerance:
                    movex = speed
                    movey = 0
                    #print("dis x: " + str(disx))
                if disy >= distance_tolerance:
                    movey = speed
                    movex = 0
                    #print("dis y: " + str(disy))
                vel_msg.linear.x = movex*self.linear_vel(goal_pose) + movey*self.linear_vel(goal_pose)
                vel_msg.linear.y = 0
                vel_msg.linear.z = 0
                self.velocity_publisher.publish(vel_msg)
                self.rate.sleep()

        if decision == 1: #turn to correct angle
            angleDiff = abs(self.pose.theta - self.steering_angle(goal_pose))
            #print("angle diff is:" + str(angleDiff)) 
            while angleDiff >= angle_tolerance:
                # Angular velocity in the z-axis.
                vel_msg.angular.x = 0
                vel_msg.angular.y = 0
                vel_msg.angular.z = self.angular_vel(goal_pose)
                self.velocity_publisher.publish(vel_msg)
                self.rate.sleep()
                angleDiff = abs(self.pose.theta - self.steering_angle(goal_pose))
                
        if decision == 2: #go along diagnol
            while self.euclidean_distance(goal_pose) >= distance_tolerance:
                vel_msg.linear.x = self.linear_vel(goal_pose)
                vel_msg.linear.y = self.linear_vel(goal_pose)
                vel_msg.linear.z = 0
                self.velocity_publisher.publish(vel_msg)
                self.rate.sleep()
                
        # Stopping our robot after the movement is over.
        vel_msg.linear.x = 0
        vel_msg.angular.z = 0
        self.velocity_publisher.publish(vel_msg)


if __name__ == '__main__':
    k=0
    S = .15
    x = TurtleBot()
    start = time.time()
    posX = 5.5444
    posY = 5.5444
    array = np.array([[5,0,0,-1,-1,0,0,1,1,0,0,-4,-4,-3.5,-3.5,-3.5,-3.5,-4,-4, 0, 0,1,1, 0, 0,-1,-1, 0, 0,5,5,0,0,-1,-1,0,0,3.5,3.5,3.5,3.5, 0, 0,-1,-1, 0, 0,5,5],
                      [0,3,3, 0, 0,9,9,0,0,3,3, 0, 0,-6.5,-6.5, 6.5, 6.5, 0, 0,-3,-3,0,0,-9,-9, 0, 0,-3,-3,0,0,3,3, 0, 0,7,7,-6 ,-6 ,  6,  6,-7,-7, 0, 0,-3,-3,0,0],
                      [0,1,0, 1, 0,1,0,1,0,1,0, 1, 0,  1 ,  2 ,  1 ,  2 , 1, 0, 1, 0,1,0, 1, 0, 1, 0, 1, 0,1,0,1,0, 1, 0,1,0, 1 , 0 ,  1,  0, 1, 0, 1, 0, 1, 0,1,0]])

    while (k<=(len(array[0,:])-1)):
        #0-straight, 1-turn, 2-diagonal
        targetx = array[0,k]*S + posX
        targety = array[1,k]*S + posY
        decision = array[2,k]
           
        x.move2goal(targetx,targety, decision)
        if decision == 0 or 2:
            posX = targetx
            posY = targety
        k += 1

    else:
        rospy.ROSInterruptException
        print("All Moves Complete")
        end = time.time()
        print(end - start)
        pass
    # If we press control + C, the node will stop.
    rospy.spin()
