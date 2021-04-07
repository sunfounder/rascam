from rascam import Ras_Cam,run_command,Joystick_Motion_type
import time
import datetime


if __name__ == "__main__":
    try:
        # clear all the jpg file
        # print("clean all the jpg file in 5 seconds later")
        print("clean all the jpg file in 5 seconds later")
        time.sleep(5)
        run_command("sudo rm /home/pi/Pictures/time_lapse_video/*.jpg")
        # print("clean finish!")
        # w : Photo width
        # h : Photo height   
        # o : Output photo file name    
        # rot : Rotation angle
        # -t : Total shooting length
        # tl : Interval between shots
        print("start to take picture")
        run_command("sudo raspistill -w 1920 -h 1440 -o /home/pi/Pictures/time_lapse_video/image_%08d.jpg  -t 750000 -tl 3000")  # 2000 = 2000ms =2s

        # r : frame rate
        # i : input file name   
        # vcodec : Video codecs   
        # The last string parameter is the output file name
        print("Making videos...")
        print("ffmpeg -r 25 -i /home/pi/Pictures/time_lapse_video/image_%08d.jpg -vcodec libx264 /home/pi/Pictures/time_lapse_video/" + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + ".mp4")
        run_command("ffmpeg -r 25 -i /home/pi/Pictures/time_lapse_video/image_%08d.jpg -vcodec libx264 /home/pi/Pictures/time_lapse_video/" + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + ".mp4") # r: FPS
        print("Finish!")
        # run_command("sudo rm /home/pi/Pictures/time_lapse_video/*.jpg")
    
    finally:
        # pass
        run_command("sudo kill $(ps aux | grep 'make_time_lapse_video.py' | awk '{ print $2 }')")