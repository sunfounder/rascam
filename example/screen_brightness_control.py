from rascam import Ras_Cam,Joystick_Motion_type,set_screen_brightness
import time



# brightness = 50
if __name__ == "__main__":
    try:

        Ras_Cam.camera_start()

        while True:
            button_type = Joystick_Motion_type()
            if button_type == 'shuttle':
                Ras_Cam.shuttle_button(True)
            elif button_type == 'up':
                # print('up')
                set_screen_brightness(100)
            elif button_type == 'down':
                set_screen_brightness(10)

    finally:
        run_command("sudo kill $(ps aux | grep 'screen_brightness_control.py' | awk '{ print $2 }')")
