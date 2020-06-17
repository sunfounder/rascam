from rascam import Ras_Cam,power_val,Joystick_Motion_Val,Joystick_Motion_type,run_command
import time

if __name__ == "__main__":
    try:
        Ras_Cam.camera_start()

        flag = False
        camera_t = None
        camera_v = None
        while True:
            press_count = 0
            while Joystick_Motion_Val('press') == 0:
                press_count+=1
                count = 0
                if press_count >= 20:
                    break
                time.sleep(0.1)
            if press_count >=20:
                flag = not flag
                # print(flag)
                Ras_Cam.show_setting(flag)

            button_type = Joystick_Motion_type()
            if button_type == 'left':
                camera_t = Ras_Cam.change_show_setting(shirt_way = 'add')
            elif button_type == 'right':
                camera_t= Ras_Cam.change_show_setting(shirt_way = 'sub')

            elif button_type == 'up':
                # print('up')
                Ras_Cam.change_setting_type_val(camera_t,0)
            elif button_type == 'down':
                # print('down')
                Ras_Cam.change_setting_type_val(camera_t,100)
            elif button_type == 'shuttle':
                Ras_Cam.shuttle_button(True)
    
    finally:
        run_command("sudo kill $(ps aux | grep 'show_and_change_camera_setting.py' | awk '{ print $2 }')")

