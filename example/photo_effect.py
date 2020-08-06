from rascam import Ras_Cam,Joystick_Motion_type,run_command
import time



if __name__ == "__main__":
    try:
        Ras_Cam.camera_start()


        while True:
            button_type = Joystick_Motion_type()
            if button_type == 'left':
                Ras_Cam.photo_effect('sub') # Move to the left.
            elif button_type == 'right':
                Ras_Cam.photo_effect('add') # Move to the right.
            elif button_type == 'shuttle':
                Ras_Cam.shuttle_button(True)
    
    finally:
        run_command("sudo kill $(ps aux | grep 'photo_effect.py' | awk '{ print $2 }')")
