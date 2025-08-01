# Jetson Scripts – Educational Mobile Robot Prototype
This directory contains the Python scripts developed for execution on the Jetson Nano, as part of the educational mobile robot prototype described in the article:
**"Construction of an Educational Prototype of a Differential Wheeled Mobile Robot"**  
Authors: Celso Márquez-Sánchez, et la.
Journal: *Hardware* (MDPI)

## Description
The scripts in this folder implement the core functionalities for real-time trajectory tracking, velocity control, and serial communication between the Jetson and the Arduino Nano.
## Script Descriptions
- `principalHardware.py`:  
  Main script that runs the control loop. It handles the execution of the trajectory, communication with the Arduino Nano, and plotting of the tracking results.
- `trajectory.py`:  
  Generates reference trajectories such as linear, circular, or sinusoidal for the robot to follow.
- `PD.py`:  
  Contains the implementation of the controller used to calculate the desired velocities based on the tracking error.

- `atan3.py`:  
  Auxiliary script that defines an extended `atan2` function with angle wrapping to ensure consistent orientation error computation.

- `test/`:  
  Directory for optional test scripts or experimental modules used during development or debugging.

## Requirements
- Jetson Nano or Jetson Orin running Ubuntu 18.04/20.04
- Python 3.6 or newer
- Required Python packages:
  - `numpy`
  - `pyserial`
  - `matplotlib`

## How to Run
1. Ensure the Arduino Nano is connected via USB and running its corresponding motor control code.
2. From the Jetson terminal, navigate to the folder containing the scripts.
3. Run the main script:
   ```bash
   sudo python3 principalHardware.py
