# Raspberry Pi Camera API

## The functions of ports can be divided into two parts: the camera-relevant functions in Ras_Cam and the assistant tool functions involving the toggle and the button.


Usage:
```python
from rascam import Ras_Cam,power_val,get_ip,Joystick_Motion_type,Joystick_Motion_Val

Ras_Cam.camera_start()    #run the camera and the screen
content_1 = "IP:" + str(get_ip())      #the displayed content is 1 and here, the port function is called to get the IP and assign it to the content 1

Ras_Cam.show_content(1, content_1, (int(content_1_x),15), content_1_color, font_size)      #the screen displays the content 1
Ras_Cam.show_content(2, "power:" + str(power_val()) + "V", (0,35), content_2_color, font_size)  #The screen displays the voltage
up_val = Joystick_Motion_Val('up')    #judge whether the joystick is toggled up; if it do this, return 0; otherwise return 1

press_val = Joystick_Motion_Val('press')    #judge whether the joystick is toggled down; if it do this, return 0; otherwise return 1

while True:
    print("type:",Joystick_Motion_type())         #get the joystick type via the interrupt mode

    # time.sleep(1)

```

## Constructors
```class Ras_Cam()```
Use Ras_Cam api to set up the camera according to your preference.

## Utils_Methods
- get_ip - return  the ip of Pi.
```python
get_ip()
```

- calibrate_imu_acc - calibrate the imu.
```python
calibrate_imu_acc()
```

- power_val - return  the power of Pi.
```python
power_val()
```

- Joystick_Motion_type - return  the joystick motion.
```python
Joystick_Motion_type()
```

- joystick_Motion_Val(motion) - return  the pin of joystick pin.
```python
joystick_Motion_Val(motion)
```

- calibrate_imu_acc() - calibrate_imu.
```python
calibrate_imu_acc()
```
## class_Ras_Cam_Methods

- camera_start() - start the camera and screen,only set once.
```python
Ras_Cam.camera_start()
```
- photo_effect(shirt_way = 'add') - change the photo effect.you can use parameter 'add' or 'sub' to control the change of effect.
```python
Ras_Cam.photo_effect(shirt_way = 'add')
```

- change_show_setting(shirt_way = 'add) - show the camera setting on the screen.you can use parameter 'add' or 'sub' to control the change of setting.
```python
Ras_Cam.change_show_setting(shirt_way = 'add')
```

- google_upload(flag) - control google_upload yes or no.
```python
Ras_Cam.google_upload(True)
```

- show_content(id_num,content,content_coordinate,content_color,font_size) - set yourself content show on screen.
```python
Ras_Cam.show_content(1,"hello world",(15,20),(255,155,240),0.7)
```

- change_setting_type_val(setting_type,setting_val) - set the camera setting
```python
Ras_Cam.change_setting_type_val("resolution",(1280,960))
```

- shuttle_button(flag) - control shuttle picture.Use True or False.
```python
Ras_Cam.shuttle_button(True)
```

- human_detect_switch(flag)
```python
Ras_Cam.human_detect_switch(True)
```

- watermark(flag)
```python
Ras_Cam.watermark(True)
```