from rascam import Ras_Cam,Joystick_Motion_type,RGB_Matrix,run_command,PWM
import time


if __name__ == "__main__":
    try:
        
        P1_Channel = PWM("P0")
        Ras_Cam.camera_start()
        # Ras_Cam.human_detect_switch(True)
        # rr = RGB_Matrix(0X74)
        i = 0
        sub_val = 1
        while True:
            i += sub_val
            if i >= 100 or i <= 0:
                sub_val *= -1
            P1_Channel.pulse_width_percent(i)
            time.sleep(0.1)


    finally:
        run_command("sudo kill $(ps aux | grep 'take_picture.py' | awk '{ print $2 }')")
