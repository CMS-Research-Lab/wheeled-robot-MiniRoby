# Arduino Nano Code – Educational Mobile Robot Prototype
This folder contains the source code developed for the **Arduino Nano** board, used in the prototype presented in the article:
**"Construction of an Educational Prototype of a Differential Wheeled Mobile Robot"**  
Authors: Celso Márquez-Sánchez, et al.  
Journal: *Hardware* (MDPI)

## Code Functionality
The code implements basic differential drive control for the robot, enabling:
- Motor control via an H-bridge driver
- Reading speed commands via serial communication
- Speed modulation using PWM

## Requirements
- Board: Arduino Nano
- Library: `PinChangeInterrupt.h`  
  > ⚠️ Note: This library must be installed before uploading the program.

## Additional Notes
- The code is intended to be used with the 3D-printed mobile robot whose design files are provided in the `stl/` folder.
- Emergency stop logic is currently declared but not implemented.
