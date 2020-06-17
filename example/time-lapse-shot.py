from rascam.utils import run_command
import time




if __name__ == "__main__":
    try:

        Ras_Cam.camera_start()

        while True:
            button_type = Joystick_Motion_type()
            if button_type == 'shuttle':
                Ras_Cam.shuttle_button(True)

    finally:
        run_command("sudo kill $(ps aux | grep 'time-lapse-shot.py' | awk '{ print $2 }')")