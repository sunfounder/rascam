from rascam import Ras_Cam,Joystick_Motion_type,RGB_Matrix,run_command
# from rgb_matrix import RGB_Matrix
import time


if __name__ == "__main__":
    try:
        Ras_Cam.camera_start()
  
        rr = RGB_Matrix(0X74)


        while True:
            button_type = Joystick_Motion_type()
            if button_type == 'shuttle':
                for i in range(9):
                    if i == 8:
                        rr.draw_line((0,0,7,0),fill=(0,255,0))
                        rr.display()
                        break
                    rr.draw_point((i,0),fill=(255,0,0))
                    rr.display()
                    time.sleep(1)
                Ras_Cam.shuttle_button(True)
                time.sleep(1)
                rr.draw_line((0,0,7,0),fill=(0,0,0))
                rr.display()
    
    finally:
        run_command("sudo kill $(ps aux | grep 'countdown photo.py' | awk '{ print $2 }')")

