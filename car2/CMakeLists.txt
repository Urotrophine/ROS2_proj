cmake_minimum_required(VERSION 3.8)
project(car2)

# 推荐启用更严格的编译警告
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# ROS2 构建系统
find_package(ament_cmake REQUIRED)

# 安装资源文件（urdf / meshes / launch / config）
install(
  DIRECTORY config launch meshes urdf rviz world
  DESTINATION share/${PROJECT_NAME}
)

# install python script so it ends up at install/lib/<pkg>/
install(PROGRAMS
  scripts/robot_description_publisher.py
  DESTINATION lib/${PROJECT_NAME}
)


ament_package()
