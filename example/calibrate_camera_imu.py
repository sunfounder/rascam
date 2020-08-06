from rascam import calibrate_imu_acc,run_command
import time




if __name__ == "__main__":
    try:

        calibrate_imu_acc() 

        while True:
            pass

    finally:
        run_command("sudo kill $(ps aux | grep 'calibrate_camera_imu.py' | awk '{ print $2 }')")
