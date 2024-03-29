from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import LaunchConfiguration, TextSubstitution
from launch import LaunchDescription
from launch_ros.actions import Node, ComposableNodeContainer
from launch_ros.descriptions import ComposableNode

def generate_launch_description():
  addThree_a = DeclareLaunchArgument(
    'addThree_a',
    default_value=TextSubstitution(text='3'),
    description='Argument for addThree_a'
  )

  addThree_b = DeclareLaunchArgument(
    'addThree_b',
    default_value=TextSubstitution(text='4'),
    description='Argument for addThree_b'
  )

  addThree_c = DeclareLaunchArgument(
    'addThree_c',
    default_value=TextSubstitution(text='4'),
    description='Argument for addThree_c'
  )

  # other way to run Node, lower level.  (can also run other executables)
  # client_node = ExecuteProcess( 
  #   cmd=['ros2', 'run', 'my_services', 'client_node', LaunchConfiguration('addThree_a'), LaunchConfiguration('addThree_b'), LaunchConfiguration('addThree_c')],
  #   output='screen'
  # )

  container = ComposableNodeContainer(
    name='my_container',
    namespace='',
    package='rclcpp_components',
    executable='component_container_mt',
    composable_node_descriptions=[
      ComposableNode(
        package='my_services',
        plugin='my_services.MinimalClientAsync',
        name='client_node',
        namespace='',
        parameters=[
          {'a': LaunchConfiguration('addThree_a')},
          {'b': LaunchConfiguration('addThree_b')},
          {'c': LaunchConfiguration('addThree_c')}
        ]
      ),
      ComposableNode(
        package='my_services',
        plugin='my_services.MinimalService',
        name='service_node',
        namespace=''
      )
    ],
    output='screen'
  )

  client_node = Node(
    package='my_services',
    executable='client_node',
    name='client_node',
    output='screen',
    parameters=[
      {'a': LaunchConfiguration('addThree_a')},
      {'b': LaunchConfiguration('addThree_b')},
      {'c': LaunchConfiguration('addThree_c')}
    ],
    arguments=[]
  )

  service_node = Node(
    package='my_services',
    executable='service_node',
    name='service_node',
    output='screen'
  )

  return LaunchDescription([
    addThree_a,
    addThree_b,
    addThree_c,
    # client_node,
    # service_node
    container
  ])

if __name__ == '__main__':
  generate_launch_description()
