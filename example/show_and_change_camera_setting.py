from rascam import Ras_Cam,power_val,Joystick_Motion_Val,Joystick_Motion_type,run_command
import time

## camera_setting,you can diy by yourself.just add new item to the dict.Like the one shown below.
camera_setting_dict = {
        "resolution":[(640,480),(1280,960),(1920,1440),(2592,1944)],    
        #"framerate 
        "rotation":[0,90 ,180 ,270],      #
        "brightness":[i for i in range(0,101)],   # 0~100  default 50
        "sharpness":[i for i in range(-100,101)],    # -100~100  default 0
        "contrast":[i for i in range(-100,101)],    # -100~100  default 0
        "saturation":[i for i in range(-100,101)],    # -100~100  default 0
        "iso":[0,100,200,320,400,500,640,800],           #Vaild value:0(auto) 100,200,320,400,500,640,800
        "exposure_compensation":[i for i in range(-10,11)],       # -25~25  default 0
        "exposure_mode":["'off'", "'auto'","'night'", "'nightpreview'", "'backlight'", "'spotlight'", "'sports'", "'snow'", "'beach'","'verylong'", "'fixedfps'", "'antishake'","'fireworks'"],       #Valid values are: 'off', 'auto' (default),'night', 'nightpreview', 'backlight', 'spotlight', 'sports', 'snow', 'beach','verylong', 'fixedfps', 'antishake', or 'fireworks'
        "meter_mode":["'average'","'spot'", "'backlit'", "'matrix'"],     #Valid values are: 'average' (default),'spot', 'backlit', 'matrix'.
        "awb_mode":["'off'", "'auto'", "'sunlight'", "'cloudy'", "'shade'", "'tungsten'", "'fluorescent'","'incandescent'", "'flash'", "'horizon'"],       #'off', 'auto' (default), ‘sunlight', 'cloudy', 'shade', 'tungsten', 'fluorescent','incandescent', 'flash', or 'horizon'.
        "hflip":[False ,True],          # Default:False
        "vflip":[False ,True],          # Default:False
        "drc_strength":["'off'", "'low'", "'medium'", "'high'"],
        "shutter_speed":[0,33333,100000]

        # "crop":[],           #Retrieves or sets the zoom applied to the camera’s input, as a tuple (x, y, w, h) of floating point
                          #values ranging from 0.0 to 1.0, indicating the proportion of the image to include in the output
                          #(the ‘region of interest’). The default value is (0.0, 0.0, 1.0, 1.0), which indicates that everything
                          #should be included.
}


if __name__ == "__main__":
    try:
        Ras_Cam.camera_start()

        flag = False
        camera_t = 'resolution'
        camera_v = (1920,1440)  # set the the init resolution 

        content_1_color = [0,255,255]   # content 2 text color

        font_size = 0.6          # content font size
 
        while True:
            press_count = 0
            while Joystick_Motion_Val('press') == 0: # Press and hold the round button for two seconds.It controls the display and exit of camera parameters
                press_count+=1
                count = 0
                if press_count >= 20:
                    break
                time.sleep(0.1)
            if press_count >= 20:
                flag = not flag
                Ras_Cam.show_setting(flag)   #show camera setting

            button_type = Joystick_Motion_type()
            while  flag:
                press_count = 0
                while Joystick_Motion_Val('press') == 0: # Press and hold the round button for two seconds.It controls the display and exit of camera parameters
                    press_count+=1
                    count = 0
                    if press_count >= 20:
                        break
                    time.sleep(0.1)
                if press_count >= 20:
                    flag = not flag
                    Ras_Cam.show_setting(flag)   #show camera setting

                button_type = Joystick_Motion_type()
                if button_type == 'left':
                    camera_t,camera_v = Ras_Cam.change_show_setting(shirt_way = 'add')   #Toggle the round button to the left or right.it will return the camera current setting type
                elif button_type == 'right':
                    camera_t,camera_v = Ras_Cam.change_show_setting(shirt_way = 'sub')

                elif button_type == 'up':
                    camera_t,camera_v = Ras_Cam.change_show_setting(shirt_way = 'None')
                    
                    setting_choice_num = len(camera_setting_dict[camera_t])
                    setting_val_index = camera_setting_dict[camera_t].index(camera_v)
                    if setting_val_index < setting_choice_num-1:
                        setting_val_index += 1

                    Ras_Cam.change_setting_type_val(camera_t,camera_setting_dict[camera_t][setting_val_index])          #change the current setting
                elif button_type == 'down':
                    camera_t,camera_v = Ras_Cam.change_show_setting(shirt_way = 'None')
                    print(camera_t,camera_v)
                    # setting_choice_num = len(camera_setting_dict[camera_t])
                    setting_val_index = camera_setting_dict[camera_t].index(camera_v)
                    if setting_val_index > 0:
                        setting_val_index -= 1

                    Ras_Cam.change_setting_type_val(camera_t,camera_setting_dict[camera_t][setting_val_index])          #change the current setting

            if button_type == 'shuttle':
                Ras_Cam.shuttle_button(True)

    
    finally:
        # pass
        run_command("sudo kill $(ps aux | grep 'show_and_change_camera_setting.py' | awk '{ print $2 }')")

