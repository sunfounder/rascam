Example Explanation (The following examples are watermarked by default. 
To close the watermark, you can check the take_picture.py example)

1. add_content_on_screen.py   -this example guides you to display the contents you want on the screen
2. Countdown photo     -this example makes you take a countdown photo once you press down the shuttle button
3. flash_light_camera     -press the shuttle button to take a photo with a camera flash. 
4. photo_effect         -toggle the joystick to left or right to switch the filter or take a photo with pressing the shuttle.
5. show_and change_camera_setting   -this example shows you the basic settings and the methods of revising settings
6. take_picture              -this is an example of taking a photo by pressing the shuttle.
7. human_face_detect.py              -a face detection example.
8. pwm_control.py              -a pwm control example.
9. screen_brightness_control.py              -a screen brightness control example.
10. take_picture_and_upload.py              -an example of taking pictures and uploading to Google.
11. make_time-lapse-video.py              -an example of a delayed picture with pressing the shuttle button and uploading to Google.
12. calibrate_camera.py    -calibrate the camera IMU.

# The Example of Start On Boot

1. cd ~
2. sudo crontab -e
3. At the bottom add @reboot python3 /home/pi/rascam/example/XXXX.py & (XXXX是你想自启动的示例名称)

# Calibration of the Camera IMU
## If the shot pictures are inverted, you may have to calibrate the IMU by following the descriptions below.

1. Run sudo python3 ~/rascam/example/calibrate_camera_imu.py
2. Hold and remain the camera up.
3. Press "s" to start your calibration
4. Separately rotate 360°along x, y, and z in a slow way.
5. Press Ctrl + c to exit the calibration.