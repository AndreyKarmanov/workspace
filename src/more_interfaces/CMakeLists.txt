cmake_minimum_required(VERSION 3.8)
project(more_interfaces)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)

#USER SPECIFIC

set(msg_files 
  "msg/AddressBook.msg"
  "msg/Num.msg"
  "msg/Sphere.msg")

set(srv_files 
  "srv/AddThreeInts.srv")

set(action_files 
  "action/Fibonacci.action")

find_package(geometry_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(
  ${PROJECT_NAME}
  ${msg_files}
  ${srv_files}
  ${action_files}
  DEPENDENCIES 
  geometry_msgs
)

ament_export_dependencies(rosidl_default_runtime)

# everything below is only needed if the package has both code and messages (not just messages)

# create Node executable ?? 
find_package(rclcpp REQUIRED)

add_executable(publish_address_book src/publish_address_book.cpp)
ament_target_dependencies(publish_address_book rclcpp)


install(TARGETS
publish_address_book
DESTINATION lib/${PROJECT_NAME})

# link against the interface
rosidl_get_typesupport_target(cpp_typesupport_target
${PROJECT_NAME} rosidl_typesupport_cpp)

target_link_libraries(publish_address_book "${cpp_typesupport_target}")
ament_package()
