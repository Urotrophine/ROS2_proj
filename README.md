```
colcon build --symlink-install
source install/setup.bash
export GZ_SIM_RESOURCE_PATH=$GZ_SIM_RESOURCE_PATH:$(ros2 pkg prefix car2)/share
ros2 launch car2 our_world.launch.py use_sim_time:=true
``` 

open a new terminal **(Please strictly follow the sequence of the following commands)** :   
Note: The last command is to deal with the problem that nav2's localization launch requies a "map" frame to set the robot's initial pose, but the "map" frame is published by the launch file itself, so we can create a fake static tf between map and odom and then set the "Fixed Frame" in rviz2 to "map" to enable nav2's initial pose estimation.
```
ros2 topic pub /arm/joint4_cmd std_msgs/msg/Float64 '{data: -3.2}' --once
ros2 topic pub /arm/joint1_cmd std_msgs/msg/Float64 '{data: 3.2}' --once
ros2 run tf2_ros static_transform_publisher   0 0 0 0 0 0 map odom use_sim_time:=true
```

open a new terminal:  
```
ros2 launch nav2_bringup localization_launch.py map:=<full/path/to/maps/map.yaml> use_sim_time:=true
params_file:=<full/path/to/config/nav2_params.yaml>
```
***After doing this, don't forget to kill the running static tf you created above!!!***

open a new terminal:  
```
ros2 launch nav2_bringup navigation_launch.py use_sim_time:=true params_file:=<full/path/to/config/nav2_params.yaml>
```
Then you should be able to navigate the robot to most of the points in the map.

To visualize the costmaps, you should press the "Add" button on the left of rviz2 control panel, and choose "add by topic" to look for "map" under "map", "global_costmap" or "local_costmap". If you would like to visualize the map under "map" created by SLAM, after you add the "map" into the panel, don't forget to change its Qos profile "Durability" to "Transient Local".

If you want to set our robot into new environments, you should do SLAM mapping firstly.  
```
colcon build --symlink-install
source install/setup.bash
export GZ_SIM_RESOURCE_PATH=$GZ_SIM_RESOURCE_PATH:$(ros2 pkg prefix car2)/share
ros2 launch car2 our_world.launch.py use_sim_time:=true
```

open a new terminal  
```
ros2 launch nav2_bringup navigation_launch.py params_file:=<full/path/to/config/nav2_params.yaml> use_sim_time:=true
```

Then open a new terminal  
```
ros2 launch slam_toolbox online_async_launch.py use_sim_time:=true
```

**Then you should change your "fixed frame" in rviz into "map".**
open a new terminal and enter:  
```
# joint4 → -3.2 rad
ros2 topic pub /arm/joint4_cmd std_msgs/msg/Float64 '{data: -3.2}' --once

# joint5 → 3.2 rad
ros2 topic pub /arm/joint5_cmd std_msgs/msg/Float64 '{data: 3.2}' --once

# joint1 → 3.2 rad
ros2 topic pub /arm/joint1_cmd std_msgs/msg/Float64 '{data: 3.2}' --once

# joint2 → 1 m（prismatic）
ros2 topic pub /arm/joint2_cmd std_msgs/msg/Float64 '{data: 1.0}' --once

# joint3 → 0 m（prismatic）
ros2 topic pub /arm/joint3_cmd std_msgs/msg/Float64 '{data: 0.0}' --once
```

Then the arm will go to the best position for keeping balance and enabling SLAM scanning.

open a new terminal and begin to ***gently*** move the robot around by yourself. ***Please control the twisting speed of the robot or the scanning result will not be valid.***  
Also, try your best to prevent the robot from rushing into the wall, or the scanning results will also be interrupted.  
```
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -p stamped:=true --remap cmd_vel:=/cmd_vel
```

When you are satisfied about your SLAM scanning results, stop the control panel and in the same terminal, run:  
```
ros2 run nav2_map_server map_saver_cli -f ~/map
```
You should find two map files in the ~/ folder. Make your maps/ directory and move(mv) the maps into maps/, and then move(mv) the maps/ under car2/.
