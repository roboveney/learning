#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import rospy
from geometry_msgs.msg import Pose2D
from sensor_msgs.msg import LaserScan
import pandas as pd

#establish ros node and publisher to velocity
def main():
    vel_pub = rospy.Publisher("/triton_lidar/vel_cmd", Pose2D, queue_size=2)
    rospy.init_node("fwd")
    rospy.Subscriber("/scan", LaserScan)
    
    data = {'Fwd':[0,0,10,0,0,0,0,-10,-1,0,0,0,0,-10,10,0,0],'Left':[10,1,0,-1,-10,-1,0,0,0,0,0,0,0,0,-1,0,0],\
            'Right':[-10,-1,0,1,10,0,0,10,1,0,0,0,1,1,-1,1,0], \
            'States':['R.TooClose','R.Close','R.Med', 'R.Far','R.TooFar','L.Close','L.Far','F.TooClose','F.Close', \
                      'F.Med', 'F.Far','RF.Close','RF.Far','O.AppWall','O.Parallel','O.AwayWall','O.Undef']}
            
    qTable = pd.DataFrame(data)

    rate = rospy.Rate(2) # 10hz
    vel_msg = Pose2D()
    vel_msg.y = 0
    Laser = LaserScan()
    count = 0


    while not rospy.is_shutdown():
        if count == 0:
            vel_msg.y += .1
            print(qTable)
            print(Laser.range_min)
        vel_pub.publish(vel_msg)
        count =1
        rate.sleep()
        
#def update():
#    cur_state =
#    
#    #define R State laser range min b/w -90, 30 deg
#    if R < 0.5:
#        cur_state = R.TooClose
#    elif 0.5 <= R < 0.6:
#        cur_state = R.Close
#    elif 0.6 <= R < 0.8:
#        cur_state = R.Med
#    elif 0.8 <= R < 1.2:
#        cur_state = R.Far
#    elif R >= 1.2:
#        cur_state = R.TooFar
#    
#    #define L State laser range min b/w 30,90 deg
#    if L < 0.5:
#        cur_state = L.Close
#    elif L >= 0.5:
#        cur_state = L.Far
#    
#    #define F State laser range min b/w -30 to 30 deg
#    if F < 0.5:
        

    
    

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass

