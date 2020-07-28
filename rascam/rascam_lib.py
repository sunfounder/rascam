import numpy as np
import cv2
import threading
import RPi.GPIO as GPIO
import time

rst = 5
# GPIO.cleanup()
GPIO.setwarnings(False)
def reset_mcu():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(rst, GPIO.OUT)
    GPIO.output(rst, 0)
    time.sleep(0.1)
    GPIO.output(rst, 1)
    time.sleep(0.1)
reset_mcu()

import os
from multiprocessing import Process, Manager

# from utils import cpu_temperature
# import imutils
import sys
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
from PIL import Image, ImageDraw, ImageFont
import rascam.tft_screen as ST7789
# import ST7789
from rascam.pwm import PWM

# import time
import numpy as np
from rascam.pin import Pin
import datetime 
# from flask import Flask, render_template, Response



# reset_mcu()

from rascam.sh3001 import Sh3001
# import time
from math import asin
import math
from rascam.adc import ADC
from rascam.google_upload import upload



sensor = Sh3001()
power_pin_adc = ADC("A2")


time_font = lambda x: ImageFont.truetype('/home/pi/rascam/rascam/Roboto-Light-2.ttf', int(x / 320.0 * 6))
text_font = lambda x: ImageFont.truetype('/home/pi/rascam/rascam/Roboto-Light-2.ttf', int(x / 320.0 * 10))
company_font = lambda x: ImageFont.truetype('/home/pi/rascam/rascam/Roboto-Light-2.ttf', int(x / 320.0 * 8))


def add_text_to_image(name, text):
    # rgba_image = image.convert('RGB')
    # text_overlay = Image.new('RGB', rgba_image.size, (255, 255, 255))
    image_target = Image.open(name)

    image_draw = ImageDraw.Draw(image_target)

    
    time_text = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    time_size_x, time_size_y = image_draw.textsize(time_text, font=time_font(image_target.size[0]))
    text_size_x, text_size_y = image_draw.textsize(text, font=text_font(image_target.size[0]))

  # 设置文本文字位置
    # print(rgba_image)
    time_xy = (image_target.size[0] - time_size_x - time_size_y, image_target.size[1] - int(1.5*time_size_y))
    text_xy = (text_size_y, image_target.size[1] - int(1.5*text_size_y))
    company_xy = (text_size_y, image_target.size[1] - int(1.5*text_size_y) - text_size_y)

  # 设置文本颜色和透明度
    image_draw.text(time_xy, time_text, font=time_font(image_target.size[0]), fill=(255, 255, 255))
    image_draw.text(company_xy, text, font=text_font(image_target.size[0]), fill=(255, 255, 255))
    image_draw.text( text_xy, "SunFounder", font=company_font(image_target.size[0]), fill=(255, 255, 255))
    # run_command("sudo rm " + str(name))
    image_target.save(name,quality=95,subsampling=0)# 



def run_command(cmd):
    import subprocess
    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = p.stdout.read().decode('utf-8')
    status = p.poll()
    return status, result

def get_ip():
    _, result = run_command("hostname -I")
    ip = result.split(" ")
    return ip[0]


def calibrate_imu_acc():
    sensor.acc_calibrate_cmd()

def power_val():
    return round(power_pin_adc.read() / 4096.0 * 3.3 * 2,2)



def imu_screen_rotate():
    # print("1")
    acc_list = sensor.sh3001_getimudata('acc','xyz')
    # print(acc_list)
    acc_list = [min(2046,i) for i in acc_list]
    acc_list = [max(-2046,i) for i in acc_list]
    # print(asin(acc_list[0] / 2100.0))
    current_angle_x = (asin(acc_list[0] / 2046.0)) / math.pi * 180
    current_angle_y = (asin(acc_list[1] / 2046.0)) / math.pi * 180
    # print((asin(acc_list[1] / 2046.0)) / math.pi * 180)
    # time.sleep(0.1)
    # print("current_angle_x: ",current_angle_x)
    # print("current_angle_y: ",current_angle_y)
    return current_angle_x,current_angle_y

effect = 0

EFFECTS = [ 
    "none",
    "negative",
    "solarize",
    "sketch",
    "denoise",
    "emboss",
    "oilpaint",
    "hatch",
    "gpen",
    "pastel",
    "watercolor",
    "film",
    "blur",
    "saturation",
    "colorswap",
    "washedout",
    "posterise",
    "colorpoint",
    "colorbalance",
    "cartoon",
    "deinterlace1",
    "deinterlace2",
]


Ras_Cam_SETTING = [
        "resolution",    #max(4056,3040)
        #"framerate 
        "rotation",      #(0 90 180 270)
    
        "brightness",    # 0~100  default 50
        "sharpness ",    # -100~100  default 0
        "contrast  ",    # -100~100  default 0
        "saturation",    # -100~100  default 0
        "iso",           #Vaild value:0(auto) 100,200,320,400,500,640,800
        "exposure_compensation",       # -25~25  default 0
        "exposure_mode",       #Valid values are: 'off', 'auto' (default),'night', 'nightpreview', 'backlight', 'spotlight', 'sports', 'snow', 'beach','verylong', 'fixedfps', 'antishake', or 'fireworks'
        "meter_mode",     #Valid values are: 'average' (default),'spot', 'backlit', 'matrix'.
        "awb_mode",       #'off', 'auto' (default), ‘sunlight', 'cloudy', 'shade', 'tungsten', 'fluorescent','incandescent', 'flash', or 'horizon'.
        "hflip",          # Default:False ,True
        "vflip",          # Default:False ,True
        # "crop",           #Retrieves or sets the zoom applied to the camera’s input, as a tuple (x, y, w, h) of floating point
                          #values ranging from 0.0 to 1.0, indicating the proportion of the image to include in the output
                          #(the ‘region of interest’). The default value is (0.0, 0.0, 1.0, 1.0), which indicates that everything
                          #should be included.
]

# RESOLOTION = [(4056,3040),(2028,1520),(2028,1080),(1012,760)]


GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.IN)
GPIO.setup(16, GPIO.IN)
GPIO.setup(13, GPIO.IN)
GPIO.setup(26, GPIO.IN)
GPIO.setup(12, GPIO.IN)
GPIO.setup(24, GPIO.IN)
GPIO.setup(6, GPIO.IN,GPIO.PUD_UP)

button_motion = 'free'

def button_up(ch):
    global button_motion
    button_motion = 'up'
    # print(button_motion)
 
def button_down(ch):
    global button_motion
    button_motion = 'down'
    # print(button_motion)

def button_left(ch):
    global button_motion
    button_motion = 'left'
    # print(button_motion)
 
def button_right(ch):
    global button_motion
    button_motion = 'right'
    # print(button_motion)

def button_press(ch):
    global button_motion
    button_motion = 'press'
    # print(button_motion)

def shuttle_press(ch):
    global button_motion
    button_motion = 'shuttle'
    # print(button_motion)

def power_press(ch):
    global button_motion
    button_motion = 'power'
    # print(button_motion)
    # print(GPIO.input(6))
    time_count = 0
    while GPIO.input(6) == 0:
        # print(GPIO.input(6))
        time_count += 1
        # print(time_count)
        if time_count > 10:
            run_command("sudo poweroff")
            break
        time.sleep(0.1)
 
GPIO.add_event_detect(25, GPIO.FALLING, callback=button_up, bouncetime=200)
GPIO.add_event_detect(16, GPIO.FALLING, callback=button_down, bouncetime=200)
GPIO.add_event_detect(13, GPIO.FALLING, callback=button_left, bouncetime=200)
GPIO.add_event_detect(26, GPIO.FALLING, callback=button_right, bouncetime=200)
GPIO.add_event_detect(12, GPIO.FALLING, callback=button_press, bouncetime=200)
GPIO.add_event_detect(24, GPIO.FALLING, callback=shuttle_press, bouncetime=200)
GPIO.add_event_detect(6, GPIO.FALLING, callback=power_press, bouncetime=200)


screen_bright_control = PWM("P9")
screen_bright_control.pulse_width_percent(50)


def set_screen_brightness(brightness):
    global screen_bright_control
    screen_bright_control.pulse_width_percent(brightness)


def Joystick_Motion_type():
    global button_motion
    if button_motion == 'up':
        button_motion = 'free'
        return 'up'
    elif button_motion == 'down':
        button_motion = 'free'
        return 'down'
    elif button_motion == 'left':
        button_motion = 'free'
        return 'left'
    elif button_motion == 'right':
        button_motion = 'free'
        return 'right'
    elif button_motion == 'press':
        button_motion = 'free'
        return 'press'
    elif button_motion == 'shuttle':
        button_motion = 'free'
        return 'shuttle'
    elif button_motion == 'power':
        button_motion = 'free'
        return 'power'
    else:
        return 'free'


def Joystick_Motion_Val(motion):
    motion = str(motion)
    if motion == "up":
        return GPIO.input(25)
    elif motion == "down":
        return GPIO.input(16)
    elif motion == "left":
        return GPIO.input(13)
    elif motion == "right":
        return GPIO.input(26)
    elif motion == "press":
        return GPIO.input(12)
    elif motion == "shuttle":
        return GPIO.input(24)
    elif motion == "power":
        return GPIO.input(6)
    else:
        raise Exception("parameter error!")

disp = ST7789.ST7789(
    port=0,
    # cs=ST7789.BG_SPI_CS_FRONT,  # BG_SPI_CSB_BACK or BG_SPI_CS_FRONT
    cs=0,  # BG_SPI_CSB_BACK or BG_SPI_CS_FRONT
    dc=22,
    rst=23,
    backlight=19,               # 18 for back BG slot, 19 for front BG slot.
    spi_speed_hz=80000000,
    width=320,
    height=240,
    rotation=180
)

WIDTH = disp.width
HEIGHT = disp.height
disp.begin()


# picture_1 = cv2.imread('/home/pi/rascam/rascam/sunfounder.jpg')
# picture_1 = picture_1[...,[2,1,0]]
# disp.display(picture_1)
# time.sleep(1)

def dis():
    i = 0
    # print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    while True:
        # img = Ras_Cam.img_array[0]
        
        # print(img.shape)
        # disp.display(Ras_Cam.img_array[0])
        # time.sleep(0.01)
        # start_time = time.time()
        disp.display(Ras_Cam.img_array[0])
        # print("FPS:",int(1 / (time.time() - start_time)))
        i +=1
        print(i)


class Ras_Cam(): 
    
    kernel_5 = np.ones((5,5),np.uint8)#4x4的卷积核
    video_source = 0
    
    detect_obj_parameter = Manager().dict()
    share_list = Manager().list()
    img_array = Manager().list(range(2))

#video
    # detect_obj_parameter['vi_fps'] = 20
    face_cascade = cv2.CascadeClassifier('/home/pi/rascam/example/haarcascade_frontalface_default.xml') 

    detect_obj_parameter['ensure_flag'] = False

#diy
    detect_obj_parameter['human_n'] = 0
    detect_obj_parameter['hdf_flag'] = False

#picture
    detect_obj_parameter['eff'] = 0
    detect_obj_parameter['setting'] = 0
    detect_obj_parameter['setting_flag'] = False
    detect_obj_parameter['setting_val'] = 0
    # detect_obj_parameter['current_setting_val'] = None
    detect_obj_parameter['setting_resolution'] = (1280,960)
    detect_obj_parameter['change_setting_flag'] = False
    detect_obj_parameter['change_setting_type'] = 'None'
    detect_obj_parameter['change_setting_val'] = 0

    detect_obj_parameter['photo_button_flag'] = False
    detect_obj_parameter['content_length'] = 0
    detect_obj_parameter['content_num'] = 0
    detect_obj_parameter['process_content_1'] = []
    detect_obj_parameter['process_si'] = []
    # detect_obj_parameter['process_dict'] = {}

    detect_obj_parameter['watermark_flag'] = True
    detect_obj_parameter['google_upload_flag'] = False
    # detect_obj_parameter['process_picture'] = True
    detect_obj_parameter['picture_path'] = '/home/pi/Pictures/rascam_picture_file/' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+ '.jpg'
    moon = cv2.imread("moon.jpg")
    resize_img = cv2.resize(moon, (320,240), interpolation=cv2.INTER_LINEAR) 


# 使用白色填充图片区域,默认为黑色
    # front_view_img.fill(255) 

    rt_img = np.ones((320,240),np.uint8)      
    img_array[0] = rt_img 


    @staticmethod
    def camera_start():
        from multiprocessing import Process
        
        
        worker_2 = Process(name='worker 2',target=Ras_Cam.camera_clone)
        worker_1 = Process(name='worker 1',target=dis)
        # worker_3 = Process(name='worker 3',target=web_camera_start)
        worker_1.start()
        worker_2.start()
        # worker_3.start()



    @staticmethod
    def photo_effect(shirt_way = 'add'):
        shirt_way = str(shirt_way)
        if shirt_way == 'add':
            Ras_Cam.detect_obj_parameter['eff'] += 1
            if Ras_Cam.detect_obj_parameter['eff'] >= len(EFFECTS):
                Ras_Cam.detect_obj_parameter['eff'] = 0
        elif shirt_way == 'sub':
            Ras_Cam.detect_obj_parameter['eff'] -= 1
            if Ras_Cam.detect_obj_parameter['eff'] < 0:
                Ras_Cam.detect_obj_parameter['eff'] = len(EFFECTS) - 1
        else:
            raise Exception("parameter error!")


    @staticmethod
    def change_show_setting(shirt_way = 'None'):
        global button_motion
        if shirt_way == 'add':
            Ras_Cam.detect_obj_parameter['setting'] += 1
            if Ras_Cam.detect_obj_parameter['setting'] >= len(Ras_Cam_SETTING):
                Ras_Cam.detect_obj_parameter['setting'] = 0

        elif shirt_way == 'sub':
            Ras_Cam.detect_obj_parameter['setting'] -= 1
            if Ras_Cam.detect_obj_parameter['setting'] < 0:
                Ras_Cam.detect_obj_parameter['setting'] = len(Ras_Cam_SETTING) - 1

        elif shirt_way == 'None':
            pass

        else:
            raise Exception("parameter error!")


        # print(Ras_Cam_SETTING[Ras_Cam.detect_obj_parameter['setting']])
        if type(Ras_Cam.detect_obj_parameter['setting_val']) == str:
            Ras_Cam.detect_obj_parameter['setting_val'] = "'" + Ras_Cam.detect_obj_parameter['setting_val'] + "'"
        return Ras_Cam_SETTING[Ras_Cam.detect_obj_parameter['setting']], Ras_Cam.detect_obj_parameter['setting_val']



    @staticmethod
    def google_upload(flag):
        # global button_motion
        Ras_Cam.detect_obj_parameter['google_upload_flag'] = flag



    @staticmethod
    def show_content(id_num,content,content_coordinate,content_color,font_size):

        cmd_test = "Ras_Cam.detect_obj_parameter['process_content_" + str(id_num) + "'" + "] = [" + "'" + str(content) + "'" + "," + str(content_coordinate)+","+str(content_color)+","+str(font_size)+"]"
        exec(cmd_test)
        if id_num > Ras_Cam.detect_obj_parameter['content_num']:
            Ras_Cam.detect_obj_parameter['content_num'] = id_num

    @staticmethod
    def watermark(flag):
        # global button_motion

        Ras_Cam.detect_obj_parameter['watermark_flag'] = flag

    @staticmethod
    def show_setting(flag):
        # global button_motion

        Ras_Cam.detect_obj_parameter['setting_flag'] = flag
        # button_motion = 'free'

    @staticmethod
    def change_setting_type_val(setting_type,setting_val):
        # global button_motion
        if setting_type == 'resolution':
            Ras_Cam.detect_obj_parameter['setting_resolution'] = setting_val
        else:
            Ras_Cam.detect_obj_parameter['change_setting_type'] = setting_type
            Ras_Cam.detect_obj_parameter['change_setting_val'] = setting_val
            Ras_Cam.detect_obj_parameter['change_setting_flag'] = True


    @staticmethod
    def shuttle_button(flag):
        # global button_motion
        Ras_Cam.detect_obj_parameter['photo_button_flag']  = flag
        # button_motion = 'free'


    @staticmethod
    def camera_clone():
        Ras_Cam.camera()     

    @staticmethod
    def human_detect_object_num():
        return Ras_Cam.detect_obj_parameter['human_n']   #objects_count


    @staticmethod
    def human_detect_switch(flag=False):
        Ras_Cam.detect_obj_parameter['hdf_flag'] = flag

    @staticmethod
    def human_detect_func(img):
        if Ras_Cam.detect_obj_parameter['hdf_flag'] == True:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
            faces = Ras_Cam.face_cascade.detectMultiScale(gray, 1.2, 5,minSize = (32, 24))
            # print(len(faces))
            Ras_Cam.detect_obj_parameter['human_n'] = len(faces)
            max_area = 0
            if Ras_Cam.detect_obj_parameter['human_n'] > 0:
                for (x,y,w,h) in faces:
                    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,255),2)
            else:
                Ras_Cam.detect_obj_parameter['human_n'] = 0
            return img
        else:
            return img

    @staticmethod
    def camera():
        global effect
        camera = PiCamera()
        camera.resolution = (320, 240)
        camera.framerate = 30
        camera.rotation = 0
    
        camera.brightness = 50    #(0 to 100)
        camera.sharpness = 0      #(-100 to 100)
        camera.contrast = 0       #(-100 to 100)
        camera.saturation = 0     #(-100 to 100)
        camera.iso = 0            #(automatic)(100 to 800)
        camera.exposure_compensation = 0   #(-25 to 25)
        camera.exposure_mode = 'auto'
        camera.meter_mode = 'average'
        camera.awb_mode = 'auto'
        camera.hflip = False
        camera.vflip = False
        camera.crop = (0.0, 0.0, 1.0, 1.0)
        rawCapture = PiRGBArray(camera, size=camera.resolution)  
        last_e ='none'
        camera_val = 0
        last_show_content_list = []
        show_content_list = []
        change_type_val  = []
        try:
            while True:
                for frame in camera.capture_continuous(rawCapture, format="rgb", use_video_port=True):
                    img = frame.array
                    img = Ras_Cam.human_detect_func(img)

                    
                    # change_camera_setting
                    if Ras_Cam.detect_obj_parameter['change_setting_flag'] == True:
                        Ras_Cam.detect_obj_parameter['change_setting_flag'] = False
                        change_setting_cmd = "camera." + Ras_Cam.detect_obj_parameter['change_setting_type'] + '=' + str(Ras_Cam.detect_obj_parameter['change_setting_val'])
                        exec(change_setting_cmd)
                        change_type_val.append(change_setting_cmd)
                    if Ras_Cam.detect_obj_parameter['content_num'] != 0:

                        for i in range(Ras_Cam.detect_obj_parameter['content_num']):
                            # print(i)
                            exec("Ras_Cam.detect_obj_parameter['process_si'] = Ras_Cam.detect_obj_parameter['process_content_" + str(i+1) + "'" + "]")
                                    # print(show_content_list)
                            # print(Ras_Cam.detect_obj_parameter['process_si'])
                            cv2.putText(img, str(Ras_Cam.detect_obj_parameter['process_si'][0]),Ras_Cam.detect_obj_parameter['process_si'][1],cv2.FONT_HERSHEY_SIMPLEX,Ras_Cam.detect_obj_parameter['process_si'][3],Ras_Cam.detect_obj_parameter['process_si'][2],2)
                    
                    if Ras_Cam.detect_obj_parameter['setting_flag'] == True:
                        # print("ss")
                        setting_type = Ras_Cam_SETTING[Ras_Cam.detect_obj_parameter['setting']]
                        if setting_type == "resolution":
                            Ras_Cam.detect_obj_parameter['setting_val'] = Ras_Cam.detect_obj_parameter['setting_resolution']
                            cv2.putText(img, 'resolution:' + str(Ras_Cam.detect_obj_parameter['setting_resolution']),(10,20),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)
                        else:
                            cmd_text = "Ras_Cam.detect_obj_parameter['setting_val'] = camera." + Ras_Cam_SETTING[Ras_Cam.detect_obj_parameter['setting']]
                            # print('mennu:',Ras_Cam.detect_obj_parameter['setting_val'])
                            exec(cmd_text)
                            cv2.putText(img, setting_type + ':' + str(Ras_Cam.detect_obj_parameter['setting_val']),(10,20),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)
                        # if RRas_Cam.detect_obj_parameter['ensure_flag'] == True:
                        #     exec("camera." + Ras_Cam_SETTING[RRas_Cam.detect_obj_parameter['setting']] + '=' + RRas_Cam.detect_obj_parameter['setting_val'])
                        #     cv2.circle(img, (10, 10), 6, (100, 0, 0), -1, cv2.LINE_AA)


                    e = EFFECTS[Ras_Cam.detect_obj_parameter['eff']]
                    
                    
                    if last_e != e:
                        camera.image_effect = e
                    last_e = e
                    if last_e != 'none':
                        cv2.putText(img, str(last_e),(0,15),cv2.FONT_HERSHEY_SIMPLEX,0.6,(204,209,72),2)

                        
                    if Ras_Cam.detect_obj_parameter['photo_button_flag'] == True:
                        camera.close()
                        break
                            
    
                    Ras_Cam.img_array[0] = img
                    rawCapture.truncate(0)


                camera = PiCamera()
                imu_x,imu_y = imu_screen_rotate()
                # print("change_type_val:",change_type_val)
                for i in change_type_val:
                    exec(i)
                
                if imu_y < 35 and imu_y >-35 and imu_x <= 90 and imu_x > 45:
                    camera.resolution = (Ras_Cam.detect_obj_parameter['setting_resolution'][1],Ras_Cam.detect_obj_parameter['setting_resolution'][0])
                    camera.rotation = 270
                elif imu_y < 35 and imu_y >-35 and imu_x < -45 and imu_x >= -90:
                    camera.resolution = (Ras_Cam.detect_obj_parameter['setting_resolution'][1],Ras_Cam.detect_obj_parameter['setting_resolution'][0])
                    camera.rotation = 90
                elif imu_y < -65 and imu_y >=-90 and imu_x < 45 and imu_x >= -45:
                    camera.resolution = Ras_Cam.detect_obj_parameter['setting_resolution']
                    camera.rotation = 180
                else:
                    camera.resolution = Ras_Cam.detect_obj_parameter['setting_resolution']

                camera.image_effect = e
                rawCapture = PiRGBArray(camera, size=camera.resolution) 
                # print("12")
                picture_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                Ras_Cam.detect_obj_parameter['picture_path'] = '/home/pi/Pictures/rascam_picture_file/' + picture_time + '.jpg'
                # print(Ras_Cam.detect_obj_parameter['picture_path']) 
                camera.capture(Ras_Cam.detect_obj_parameter['picture_path'])
                # cv2.imread()
                if Ras_Cam.detect_obj_parameter['watermark_flag'] == True:
                    add_text_to_image(Ras_Cam.detect_obj_parameter['picture_path'],'Shot by Rascam')

                if Ras_Cam.detect_obj_parameter['google_upload_flag'] == True:
                    upload(file_path='/home/pi/Pictures/rascam_picture_file/', file_name=picture_time + '.jpg')

                #init again
                camera.close()
                camera = PiCamera()
                camera.resolution = (320,240)
                camera.image_effect = e
                rawCapture = PiRGBArray(camera, size=camera.resolution) 
                Ras_Cam.detect_obj_parameter['photo_button_flag'] = False
                   
        finally:
            camera.close()