# User_Diy_Manuals

## This document is used to teach you how to DIY some of the software functions and Explanation examples.

### Common Functions

```python
1. Ras_Cam.camera_start()
# This function is used to start the camera, basically it is used in every example, for the protection of the Raspberry Pi, as long as this function is used, you can press and hold the power button for two seconds to let the Raspberry Pi first normal shutdown, and then after the Raspberry Pi is finished shutting down, finally press the power button twice in a row to directly shut down the power

2. Ras_Cam.shuttle_button(True)  
# This function is used to implement the photo function, using software to achieve the shutter press action.All the pictures was in the Path: /home/pi/Pictures/rascam_picture_file/

3. Ras_Cam.watermark(True)  
# Turn on the function to add watermarks to photos

4. Ras_Cam.clarity_val()
# This function will return a picture sharpness reference value (the larger the return value, the clearer the picture), when you use the RPI HQ Camera, you will need to use this function to facilitate the adjustment of the focus

5. Joystick_Motion_type()
# This function will return a state of the current joystick, type string, such as "'left", "right", "up", "down", "shuttle", "press", "power"

6. Joystick_Motion_Val('press')
# This function will return whether the rocker action corresponding to the incoming parameters is true, if true, it returns 1, otherwise it returns 0. (The incoming parameters can be the above 5 strings)

7.Ras_Cam.horizontal_line(True)
# Turn on the function to add horizontal line to the screen
```
### Diy Functions
1. add_content_on_screen.py:This example is to teach you how to display some content you want on the screen, this example shows the detected values of the two ADCs, as well as the Raspberry Pi IP and camera voltage

```python
Ras_Cam.show_content(id_num,content,content_coordinate,content_color,font_size)
# The first parameter is the serial number of the content, each time a Ras_Cam.show_content is added, the serial number of the next content must be added by one
# The second parameter is the content you want to display
# The third parameter is the coordinates of the content, which is a turple(15,25)
# The fourth parameter is the color of the content, which is a list[255,0,0]
# The fifth is the font size, the best range is 0.5 ~ 0.8
```

2. calibrate_camera_imu.py:This example is to teach you how to calibrate the camera's IMU sensor, when your photos are inverted, you need to use this example, calibration method, please refer to page 50 of the manual
```python
calibrate_imu_acc()
```

3. countdown_photo.py:This example mainly shows how to countdown to take a picture and how to light up the light bar, when the shuttle button is pressed, the lights of the light bar will light up one by one, and when the red light is finally lit up, a picture will be taken

```python
light_bar = RGB_Matrix(0X74) 
light_bar.draw_line((1,8),fill=(0,255,0))  #Set the first light to the eighth light, fill color (fill=(R,G,B))
light_bar.draw_point((2),fill=(255,0,0))   #Set the first light, fill color (fill=(R,G,B))
light_bar.display()   #Light up the set lights
```

4. human_face_detect.py:This example is used to demonstrate the face detection function, when a face is detected, the light bar will turn green, otherwise the light bar is red

```python
Ras_Cam.human_detect_switch(True) #Turn on the face recognition function

Ras_Cam.human_detect_object_num() #This function is used to return the number of faces detected
```

5. make_time_lapse_video.py：This example is for time lapse photography, if it runs successfully, it will generate a 1920 x 1440 25 FPS 10s video at path (/home/pi/Pictures/time_lapse_video) 

6. photo_effect.py:This example is used to demonstrate the toggle filter function
```python
Ras_Cam.photo_effect('sub') # Left shift switch.

Ras_Cam.photo_effect('add') # Right shift switch.
```

7. pwm_control.py：This example is used to demonstrate the PWM output function, please read PWM.md for details on how to use it

8. screen_brightness_control.py：This example is used to demonstrate the ability to change the screen brightness
```python
set_screen_brightness(100)  # set screen brightness (0~100).
```

9. show_and_change_camera_setting.py：This example is used to adjust some adjustable parameters of the camera in real time.The menu will be displayed or undisplayed after you press the joystick for two seconds. and the horizontal line will be displayed or undisplayed after you push up the joystick for two seconds.You can take a picture with the shuttle button when the parameter setting is launched
```python
Ras_Cam.show_setting(True) # display the setting of camera 
Ras_Cam.show_setting(False) # undisplay the setting of camera               
```

10. take_picture_and_upload.py:This example is used to teach you how to take photos and upload them to google drive.
```python
Ras_Cam.google_upload(True) # Open google drive upload function
```

11. take_picture.py:This example shows the use of the function Ras_Cam.clarity_val(This func was for the HQ camera), which allows you to take pictures with the shuttle button


