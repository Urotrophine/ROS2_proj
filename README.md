Please focus on the "odom.launch.py" file in the "launch" directory, because nav2 is now integrated and it is the only way you can launch the simulation with nav2!
```
colcon build
source install/setup.bash
ros2 launch car2 odom.launch.py use_sim_time:=true
``` 

//open a new terminal ***(VERY IMPORTANT, PLEASE REMEMBER TO DO THIS!!!)***
```
ros2 run tf2_ros static_transform_publisher 0 0 0 0 0 0 map odom
```

//open a new terminal  
```
ros2 launch nav2_bringup navigation_launch.py params_file:=<full/path/to/config/nav2_params.yaml>
```

To visualize the costmaps, you should press the "Add" button on the left of rviz2 control panel, and choose "add by topic" to look for "map" under "global_costmap" or "local_costmap".
