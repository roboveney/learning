#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import rospy
from geometry_msgs.msg import Pose2D
import pandas as pd

#establish ros node and publisher to velocity
def main():
    vel_pub = rospy.Publisher("/triton_lidar/vel_cmd", Pose2D, queue_size=2)
    rospy.init_node("fwd")

    data = {'Fwd':[0,0,10,0,0,0,0,-10,-1,0,0,0,0,-10,10,0,0],'Left':[10,1,0,-1,-10,-1,0,0,0,0,0,0,0,0,-1,0,0],\
            'Right':[-10,-1,0,1,10,0,0,10,1,0,0,0,1,1,-1,1,0], \
            'States':['R.TooClose','R.Close','R.Med', 'R.Far','R.TooFar','L.Close','L.Far','F.TooClose','F.Close', \
                      'F.Med', 'F.Far','RF.Close','RF.Far','O.AppWall','O.Parallel','O.AwayWall','O.Undef']}
            
    qTable = pd.DataFrame(data)

    rate = rospy.Rate(2) # 10hz
    vel_msg = Pose2D()
    vel_msg.y = 0
    count = 0

#robot continues to accelerate forward
    while not rospy.is_shutdown():
        if count == 0:
            print(qTable)
            vel_msg.y += .1
            
        vel_pub.publish(vel_msg)
        count += 1
        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass

