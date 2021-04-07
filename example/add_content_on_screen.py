from rascam import Ras_Cam,power_val,getIP,run_command,ADC
import time


if __name__ == "__main__":
    try:
        adc_channel_1 = ADC("A0")  # only two adc channel ("A0" OR "A1")
        adc_channel_2 = ADC("A1")  
        counter_num = 0            
        content_1_x = 0
        content_1_color = [255,0,255]   # content 1 text color ([R,G,B])
        content_2_color = [0,255,255]   # content 2 text color
        content_3_color = [255,255,0]   # content 3 text color
        font_size = 0.5    # content font size   (The best range is 0.5 ~ 0.8)

        Ras_Cam.camera_start()   # start camera and screen
        content_1 = "IP: " + str(getIP())       # get the ip of Pi

        while True:
            #show content
            Ras_Cam.show_content(1, content_1, (int(content_1_x),15), content_1_color, font_size)   # the first aram must have, and The different content should be sorted in order(start from 1)
            Ras_Cam.show_content(2, "camera power: " + str(power_val()) + "V", (0,35), content_2_color, font_size)
            Ras_Cam.show_content(3, "ADC_1: " + str(adc_channel_1.read()), (0,55), content_3_color, font_size)
            Ras_Cam.show_content(4, "ADC_2: " + str(adc_channel_2.read()), (0,75), content_3_color, font_size)
    finally:
        run_command("sudo kill $(ps aux | grep 'add_content_on_screen.py' | awk '{ print $2 }')")
