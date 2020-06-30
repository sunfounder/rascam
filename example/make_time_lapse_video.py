from rascam.utils import run_command
import time


if __name__ == "__main__":
    try:
        # clear all the jpg file
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
        run_command("raspistill -w 1280 -h 960 -o image_%08d.jpg -rot 180 -t 6000 -tl 2000")  # 2000 = 2000ms =2s

        # r : frame rate
        # i : input file name   
        # vcodec : Video codecs   
        # The last string parameter is the output file name
        print("Making videos...")
        run_command("ffmpeg -r 25 -i image_%8d.jpg -vcodec libx264 " + "my_video" + ".mp4")
        print("Finish!")
    
    finally:
        run_command("sudo kill $(ps aux | grep 'make_time_lapse_video.py' | awk '{ print $2 }')")