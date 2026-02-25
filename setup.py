from os import path, listdir, geteuid, environ
import sys
import time
import threading

errors = []
here = path.abspath(path.dirname(__file__))

APT_DEPENDENCIES = [
    "python3-pip",
    "ffmpeg",
    "git-core",
    "python3-rpi.gpio",
    "python3-spidev",
    "python3-pip",
    "python3-pil",
    "python3-numpy",
    "sysstat",
    "i2c-tools",
    "python3-picamera2",
    "python3-opencv",
    "lgpio",
]

# define color print
# =================================================================
def warn(msg, end='\n', file=sys.stdout, flush=False):
    print(f'\033[0;33m{msg}\033[0m', end=end, file=file, flush=flush)

def error(msg, end='\n', file=sys.stdout, flush=False):
    print(f'\033[0;31m{msg}\033[0m', end=end, file=file, flush=flush)

# check if run as root
# =================================================================
if geteuid() != 0:
    warn("Script must be run as root. Try \"sudo python3 install.py\".")
    sys.exit(1)

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

def run_command(cmd=""):
    import subprocess
    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = p.stdout.read().decode('utf-8')
    status = p.poll()
    return status, result

at_work_tip_sw = False
def working_tip():
    char = ['/', '-', '\\', '|']
    i = 0
    global at_work_tip_sw
    while at_work_tip_sw:  
            i = (i+1)%4 
            sys.stdout.write('\033[?25l') # cursor invisible
            sys.stdout.write('%s\033[1D'%char[i])
            sys.stdout.flush()
            time.sleep(0.5)

    sys.stdout.write(' \033[1D')
    sys.stdout.write('\033[?25h') # cursor visible 
    sys.stdout.flush() 

def do(msg="", cmd=""):
    print(" - %s... " % (msg), end='', flush=True)
    # at_work_tip start 
    global at_work_tip_sw
    at_work_tip_sw = True
    _thread = threading.Thread(target=working_tip, daemon=True)
    _thread.start()
    # process run
    status, result = eval(cmd)
    # print(status, result)
    # at_work_tip stop
    at_work_tip_sw = False
    while _thread.is_alive():
        time.sleep(0.1)
    # status
    if status == 0 or status == None or result == "":
        print('Done')
    else:
        print('Error')
        errors.append("%s error:\n  Status:%s\n  Error:%s" %
                      (msg, status, result))

# Get 1000 username
USERNAME = run_command("getent passwd 1000 | cut -d: -f1")[1].strip()

def install():
    is_direct_run = environ.get('RASCAM_INSTALL') == '1'
    if not is_direct_run:
        return
    
    print("Install Rascam")
    print("Install dependency")
    do(msg="update apt-get",
        cmd='run_command("apt-get update")')
    deps = " ".join(APT_DEPENDENCIES)
    do(msg="install apt dependencies",
        cmd=f'run_command("apt-get install {deps} -y")')
    do(msg="install rascam package",
        cmd='run_command("pip3 install . --break-system-packages")')
    do(msg="uninstall RPi.GPIO",
        cmd='run_command("pip3 uninstall RPi.GPIO -y --break-system-packages")')

    print("Setup interfaces")
    do(msg="turn on I2C", cmd='run_command("raspi-config nonint do_i2c 0")')
    do(msg="turn on SPI", cmd='run_command("raspi-config nonint do_spi 0")')

    if "Pictures" not in listdir(f"/home/{USERNAME}"):
        do(msg="create Pictures directory",
            cmd=f'run_command("mkdir /home/{USERNAME}/Pictures/")')
    if "rascam_picture_file" not in listdir(f"/home/{USERNAME}/Pictures"):
        do(msg="create rascam_picture_file directory",
            cmd=f'run_command("mkdir /home/{USERNAME}/Pictures/rascam_picture_file")')
        do(msg="change directory own",
            cmd=f'run_command("sudo chown -R {USERNAME}:{USERNAME} /home/{USERNAME}/Pictures/rascam_picture_file/")')   
    if "time_lapse_video" not in listdir(f"/home/{USERNAME}/Pictures"):
        do(msg="create time_lapse_video directory",
            cmd=f'run_command("sudo mkdir /home/{USERNAME}/Pictures/time_lapse_video")')  
        do(msg="change directory own",
            cmd=f'run_command("sudo chown -R {USERNAME}:{USERNAME} /home/{USERNAME}/Pictures/time_lapse_video/")')  

    do(msg="copy rascam-config",
        cmd=f'run_command("sudo cp ./data/config /home/{USERNAME}/.rascam_config")')
    do(msg="change directory owner",
        cmd=f'run_command("sudo chown -R {USERNAME}:{USERNAME} /home/{USERNAME}/.rascam_config")')

    if len(errors) == 0:
        print("Setup Finished")
        input_val = input('If you want to reboot please press y, if not press n: ')
        while input_val not in ['y', 'n']:
            input_val = input('Please press y or n: ')
        if input_val == 'y':
            do(msg="System reboot now",
            cmd='run_command("reboot")')
        elif input_val == 'n':
            print("reboot cancel")
    else:
        print("\n\nError happened in install process:")
        for error in errors:
            print(error)
        print("Try to fix it yourself, or contact service@sunfounder.com with this message")

if len(sys.argv) > 1 and sys.argv[1] == "install":
    environ['RASCAM_INSTALL'] = '1'
    install()
else:
    from setuptools import setup
    setup()
