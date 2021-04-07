from rascam import Ras_Cam,Joystick_Motion_type,run_command
import time




if __name__ == "__main__":
    try:

        Ras_Cam.camera_start()   #start camera screen
        Ras_Cam.watermark(True)  #watermark switch

        content_1_color = [0,255,255]   # content_text_1 color
        font_size = 0.6          # content font size
        font_coordinates = (10,22)
        while True:
            button_type = Joystick_Motion_type()
            if button_type == 'shuttle':
                Ras_Cam.shuttle_button(True)   #control the shutlle
            # elif button_type == 'press':
            #     Ras_Cam.video_flag(False)   #control the shutlle
            
            Ras_Cam.show_content(1, "clarity: " + str(Ras_Cam.clarity_val()), font_coordinates, content_1_color, font_size)  # show claritysss(you can add this func to onther example,Especially Raspberry Pi High Quality Camera)
           
    finally:
        run_command("sudo kill $(ps aux | grep 'take_picture.py' | awk '{ print $2 }')")
