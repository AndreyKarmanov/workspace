from my_services.launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import LaunchConfiguration, TextSubstitution

def generate_launch_description():
  addTwo_a = DeclareLaunchArgument(
    'addTwo_a',
    default_value=TextSubstitution(text='3'),
    description='Argument for addTwo_a'
  )

  addTwo_b = DeclareLaunchArgument(
    'addTwo_b',
    default_value=TextSubstitution(text='4'),
    description='Argument for addTwo_b'
  )

  client_node = ExecuteProcess(
    cmd=['ros2', 'run', 'my_services', 'client_node', LaunchConfiguration('addTwo_a'), LaunchConfiguration('addTwo_b')],
    output='screen'
  )

  service_node = ExecuteProcess(
    cmd=['ros2', 'run', 'my_services', 'service_node'],
    output='screen'
  )

  return LaunchDescription([
    addTwo_a,
    addTwo_b,
    client_node,
    service_node
  ])

if __name__ == '__main__':
  generate_launch_description()
