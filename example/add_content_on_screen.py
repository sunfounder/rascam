from rascam import Ras_Cam,power_val,get_ip,run_command,ADC
import time


if __name__ == "__main__":
    try:
        adc_channel_1 = ADC("A0")
        adc_channel_2 = ADC("A1")  ##only two adc channel
        counter_num = 0            
        content_1_x = 0
        content_1_color = [255,0,255]   ##content 1 text color
        content_2_color = [0,255,255]   ##content 2 text color
        content_3_color = [255,255,0]   ##content 3 text color
        content_4_color = [0,255,0]   ##content 3 text color
        font_size = 0.6     ##content font size
        screen_width = 320

        Ras_Cam.camera_start()   #start camera
        content_1 = "IP:" + str(get_ip())       #get the ip of Pi
        # print("a")
        while True:
            counter_num+=1
            content_1_x += 0.2
            if content_1_x > screen_width:
                content_1_x = 0
            #show content
            Ras_Cam.show_content(1, content_1, (int(content_1_x),15), content_1_color, font_size)   
            Ras_Cam.show_content(2, "power:" + str(power_val()) + "V", (0,35), content_2_color, font_size)
            Ras_Cam.show_content(3, "counter:" + str(counter_num), (0,55), content_3_color, font_size)
            Ras_Cam.show_content(4, "ADC_1:" + str(adc_channel_1.read()), (0,75), content_4_color, font_size)
            Ras_Cam.show_content(5, "ADC_2:" + str(adc_channel_2.read()), (0,95), content_4_color, font_size)
    finally:
        run_command("sudo kill $(ps aux | grep 'add_content_on_screen.py' | awk '{ print $2 }')")
