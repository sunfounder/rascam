from rascam import Ras_Cam,run_command,Joystick_Motion_type
import time
import datetime


if __name__ == "__main__":
    try:
        # clear all the jpg file
        # Ras_Cam.camera_start()
        # print("press shuttle to start")
        # while True:
        #     button_type = Joystick_Motion_type()  # get joystick motion
        #     if button_type == 'shuttle':
        #         break

        print("clean all the jpg file in 5 seconds")
        time.sleep(5)
        run_command("sudo rm *.jpg")
        # print("clean finish!")
        # w : Photo width
        # h : Photo height   
        # o : Output photo file name    
        # rot : Rotation angle
        # -t : Total shooting length
        # tl : Interval between shots
        print("start to take picture")
        run_command("raspistill -w 1920 -h 1440 -o image_%08d.jpg  -t 600000 -tl 2000")  # 2000 = 2000ms =2s

        # r : frame rate
        # i : input file name   
        # vcodec : Video codecs   
        # The last string parameter is the output file name
        print("Making videos...")
        run_command("ffmpeg -r 25 -i image_%8d.jpg -vcodec libx264 time_lapse.mp4") # r: FPS
        print("Finish!")
    
    finally:
        # pass
        run_command("sudo kill $(ps aux | grep 'make_time_lapse_video.py' | awk '{ print $2 }')")