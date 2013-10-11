Project Summary
==============

Goals Achieved
-------------
Goal1: Write Python code to connect to a single robot (including)
       acquiring image data and movement control.

Goal2: Separate code in nodes, and run them individually by using ROS.
       
Goal3: Publish robot data in the network (such as image data) so that
       other nodes can utilize that data (for optical flow, etc.).

Goal4: Created a simple Kivy GUI in order to display published image
       from the rover and drive the robot around.

Future Goals
-----------
1) We want to change some publish/subscriber implementation to
   Service/Client implementation. This might be more efficient
   than to permanently publish data over the network, especially
   when the data is not needed by any node. 

2) Implement PWM code on the br_control node.

3) Implement a Optical Flow node to be used for path planning
   (including finding out if running out of battery based on the
   optical flow). This node shall be written in C++ for performance.
   ROS/OpenCV already have Optical Flow code.

4) Connect to multiple robots autonomously. This could be achieved
   reading the out of each NIC after they been connected to the robot
   Python can read this out.

5) Implement hand and gesture recognition code using ROS and the Kinect.
   There is already code in ROS and OpenNI to achieve this.
   
6) Implement point to goal features.

7) Send robots to the pointed to location.

8) Select an specific robot and send it to a specific goal, while the other
   robot (s) stay in the same place or are sent to another specific location.
