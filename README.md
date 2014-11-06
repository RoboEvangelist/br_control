# This is a ROS package to control one or more Brookstone Rovers v0.0.1 

> # Prerequisites:
> 1. Working knowledge of the [Robot Operating System (ROS)](http://www.ros.org/)
> 2. [Brookstone Rover(s) v1.0](http://www.amazon.com/Rover-App-Controlled-Tank-Night-Vision/dp/B005OQYOB6)
> 3. A wifi dongle/card per rover. These rovers create their own ad-hoc network, therefore you must connect to the rovers the same way you would connect to a router, for instance
> 4. [Ubuntu Linux OS](http://www.ubuntu.com/download/desktop) - tested with v13.04 Raring Ringtail 64 bits
> 5. [ROS](http://wiki.ros.org/ROS/Installation) - tested with ROS Hydro Medusa
> 6. [Kivy](http://kivy.org/docs/installation/installation-linux.html) GUI library - tested with v1.7.1
> 6. [Cython](http://kivy.org/docs/installation/installation-linux.html) GUI library installation - installed with v0.17.1

> # Installation:
> After installing [ROS](http://wiki.ros.org/ROS/Installation) and [Kivy](http://kivy.org/docs/installation/installation-linux.html), follow steps 1 through 4 from the [Beginner Level](http://wiki.ros.org/ROS/Tutorials) tutorials on the ROS website to create a workspace called catkin _ ws, and then create and build a package.
> Once the previous step is completed, you can checkout the br _ swarm _ rover repository into the workspace folder like this:
>
>      /path to workspace/catkin _ ws/src 
>
and from a terminal do 
>
>      source /path to workspace/catkin _ ws/devel/setup.bash 
>
> to add the ROS path of the br _ swarm _ rover into you .bashrc file

> # Use instructions:
> 1. Connect additional wifi dongles to your computer if needed (your computer should have at least one by default).
> 2. Turn on **one robot at a time**, and connect to it with the wifi dongle (or just with your computer's built in wifi card if only one robot is available). Generally, the rovers' default SSID, or network name, starts with "AC13" followed by its MAC address.
> 4. Then, on the terminal launch the meta-server and GUI like this (assuming your package was correctly added to your ROS path):
>
>     roslaunch br_swarm_rover br_start.launch
>
>
> Enjoy!!!
