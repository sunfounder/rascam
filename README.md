# The RPi-Based Camera
## Usage
The camera is compatible with the newly released HQ camera and the older RPi official v2 camera module. This RPi-based camera has a joystick, two buttons, two ADC and PWM ports, three I2C ports and one serial port. 
- Button 1: At the upper left is the POWER button. After the programs run, long pressing for 1s can switch off the camera and then pressing two more times can power off.
- Button 2: Above the joystick is a rectangular button named shuttle whose functions can be defined by users.
- Joystick: It can be toggled up, down, left, right and center and its functions can be defined by yourself.

## Function Description(Refer to Example)
- Function 1: Display the user-defined information, including the power voltage, ADC, and the sensor plugged via I2C. 
- Function 2: DIY your own camera via the joystick. Call the camera setting api function that you like and not use the command line.
- Function 3: The modules of RGB strips can be defined by users.
- Function 4: Upload to Google Cloud.
- Function 5: samba files sharing.
- Function 6: Face detection.
