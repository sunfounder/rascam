from rascam import run_command
from rascam.utils import get_username
import time
import datetime

USERNAME = get_username()

if __name__ == "__main__":
    try:
        # clear all the jpg file
        # print("clean all the jpg file in 5 seconds later")
        print("clean all the jpg file in 5 seconds later")
        time.sleep(5)
        run_command(f"sudo rm /home/{USERNAME}/Pictures/time_lapse_video/*.jpg")
        # print("clean finish!")
        # w : Photo width
        # h : Photo height   
        # o : Output photo file name    
        # rot : Rotation angle
        # -t : Total shooting length
        # tl : Interval between shots
        print("start to take picture")
        run_command(f"sudo raspistill -w 1920 -h 1440 -o /home/{USERNAME}/Pictures/time_lapse_video/image_%08d.jpg  -t 750000 -tl 3000")  # 2000 = 2000ms =2s

        # r : frame rate
        # i : input file name   
        # vcodec : Video codecs   
        # The last string parameter is the output file name
        print("Making videos...")
        cmd = f"ffmpeg -r 25 -i /home/{USERNAME}/Pictures/time_lapse_video/image_%08d.jpg -vcodec libx264 /home/{USERNAME}/Pictures/time_lapse_video/" + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + ".mp4"
        print(cmd)
        run_command(cmd) # r: FPS
        print("Finish!")
        # run_command(f"sudo rm /home/{USERNAME}/Pictures/time_lapse_video/*.jpg")
    
    finally:
        # pass
        run_command("sudo kill $(ps aux | grep 'make_time_lapse_video.py' | awk '{ print $2 }')")