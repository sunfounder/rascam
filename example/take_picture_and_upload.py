from rascam import Ras_Cam,Joystick_Motion_type
import time




if __name__ == "__main__":
    try:

        Ras_Cam.camera_start()
        Ras_Cam.google_upload(True)
        while True:
            button_type = Joystick_Motion_type()
            if button_type == 'shuttle':
                Ras_Cam.shuttle_button(True)

    finally:
        run_command("sudo kill $(ps aux | grep 'take_picture.py' | awk '{ print $2 }')")
