from rascam import Ras_Cam,Joystick_Motion_type,RGB_Matrix,run_command
import time




if __name__ == "__main__":
    try:
        Ras_Cam.camera_start()
        rr = RGB_Matrix(0X74)


        while True:
            button_type = Joystick_Motion_type()
            if button_type == 'shuttle':
                rr.draw_line([0,0,7,0],fill=(255,255,255))
                rr.display() # open the rgb
                time.sleep(0.5)
                Ras_Cam.shuttle_button(True)
                time.sleep(0.5)
                rr.draw_line([0,0,7,0],fill=(0,0,0)) # close the rgb
                rr.display()

    finally:
        run_command("sudo kill $(ps aux | grep 'flash_light_camera.py' | awk '{ print $2 }')")