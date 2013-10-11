.. br_swarm documentation master file, created by
   sphinx-quickstart on Thu Oct 10 23:03:40 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to br_swarm's documentation!
====================================

This is the main documentation for the Brookstone Rover project.
The main porpuse of this project is to create an autonomous system
capable of recognizing hand gesture commands from a human user.
These hand gesture commands include point goal (e.g. pointing to
an object that the human user need, such as a tool), and intention
recognition (grabing, reaching towards a tool). Once the system
recognizes the gestures or intensions, the robots can then move to
the desired goal point, or move towards the tool the human needs,
and bring the tool to the human.

Requirements:

- Linux operating system (so far tested only with Ubuntu 12.10.02)
- Robot Operating System (ROS - Hydro or above to connect to multiple robots)
- Python 3.0 or above (necessary for connection to multiple robots with ROS)
- Brookstone Rovers (so far only tested with v1.0)
- Kivy GUI library
- A wifi dongle (Network interface Card or NIC) per robot


Contents:

.. toctree::
   :maxdepth: 2

   project
   code


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

A Subpoint
----------
This is my idea.

A subsubpoint
+++++++++++++
This is a smaller idea.
