1.add_content_on_screen.py   ##该实例功能是交用户如何在屏幕展示自己想要的内容
2.Countdown photo     ##该实例功能是实现倒计时拍照
3.flash_light_camera     ##按下shuttle键实现闪光灯拍照
4.photo_effect         ##左右摇杆控制滤镜切换，shuttle拍照
5.show_and change_camera_setting   ##该实例是展示相机的基础设置，和如何设置相机设置
6.take_picture              ##拍照实例，shuttle键
7.human_face_detect.py              ##人脸识别实例
8.pwm_control.py              ##pwm控制实例
9.screen_brightness_control.py              ##屏幕亮度控制实例
10.take_picture_and_upload.py              ##拍照实例，并上传google
11.time-lapse-shot.py              ##拍照实例，并上传google
12.calibrate_camera.py    ##校准相机IMU

# 示例开机自启动
1. cd ~
2. sudo crontab -e
3. 在最下面添加: @reboot python3 /home/pi/rascam/example/XXXX.py & (XXXX是你想自启动的示例名称)

# 相机IMU校准
## 如果相机拍出来的画面是颠倒的，则可能需要校准IMU，如需校准，请按如下步骤：
1. 执行sudo python3 ~/rascam/example/calibrate_camera_imu.py
2. 举起相机不动
3. 按下键盘s开始校准
4. 缓慢的沿xyz三个方向各旋转360度
5. 校准完按下Ctrl + c退出校准即可