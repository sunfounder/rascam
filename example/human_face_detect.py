from rascam import Ras_Cam,Joystick_Motion_type,RGB_Matrix,run_command
import time




if __name__ == "__main__":
    try:

        Ras_Cam.camera_start()
        Ras_Cam.human_detect_switch(True) # open the human_face_detect func.
        rr = RGB_Matrix(0X74)

        while True:
            human_face_num = Ras_Cam.human_detect_object_num()
            # print("detect face number:",)
            if human_face_num > 0:
                print("I find %d people !!!" % human_face_num)
                rr.draw_line((1,8),fill=(0,255,0))
                rr.display()
            else:
                rr.draw_line((1,8),fill=(255,0,0))
                rr.display()

            button_type = Joystick_Motion_type()
            if button_type == 'shuttle':
                Ras_Cam.shuttle_button(True)


    finally:
        run_command("sudo kill $(ps aux | grep 'take_picture.py' | awk '{ print $2 }')")
