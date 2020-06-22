# 树莓派相机接口

## 接口函数说明，接口函数分为两个部分，一个是Ras_Cam这个类里面的和相机相关的函数，另一个是摇杆，按键等的辅助工具函数

Usage:
```python
from rascam import Ras_Cam,power_val,get_ip,Joystick_Motion_type,Joystick_Motion_Val

Ras_Cam.camera_start()    #启动相机及屏幕
content_1 = "IP:" + str(get_ip())      #要展示的内容1，此处是使用获取IP的接口函数获取IP地址，并赋值给内容1

Ras_Cam.show_content(1, content_1, (int(content_1_x),15), content_1_color, font_size)      #在屏幕显示内容1的内容
Ras_Cam.show_content(2, "power:" + str(power_val()) + "V", (0,35), content_2_color, font_size)  #在屏幕显示电压
up_val = Joystick_Motion_Val('up')    #获取摇杆是否上推,假如按下，返回0，没有上推，返回1

press_val = Joystick_Motion_Val('press')    #获取摇杆是否按下,假如按下，假如按下，返回0，没有按下，返回1

while True:
    print("type:",Joystick_Motion_type())         #中断方式获取摇杆的类型
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