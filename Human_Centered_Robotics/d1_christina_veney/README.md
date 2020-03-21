# P2-D1_README

-copy the entire folder into the ~/catkin_ws/src file of a computer that is set up for ROS and has the Stingray-Simulation package loaded and sourced as well. 

	$source /opt/ros/melodic/setup.bash
	$source ~/Stingray-Simulation/catkin_ws/devel/setup.bash
	$source ~/Stingray-Simulation/stingray_setup.bash

-run catkin_make and source the build
-run the following line of code

	$ roslaunch d1_christina_veney wall_follow_bot.launch world:=maze_world_camera.world


-Qtables can be seen at the top of the code as pandas data tables. The first was the initial guess and the second was the convergence after training. 

-the current speed of the robot was increased after finding the converged Qtable. 

