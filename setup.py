# Always prefer setuptools over distutils
Domain Name
TRACES.COM
Registry Domain ID
26709_DOMAIN_COM-VRSN
Registrar WHOIS Server
whois.networksolutions.com
Registrar URL
http://networksolutions.com
Updated Date
2022-05-28T17:55:09Z
Creation Date
1996-05-29T04:00:00Z
Registrar Registration Expiration Date
2032-05-28T04:00:00Z
Registrar
Network Solutions, LLC
Registrar IANA ID
2
Reseller
Domain Status
clientTransferProhibited https://icann.org/epp#clientTransferProhibited
Registry Registrant ID
Registrant Name
PERFECT PRIVACY, LLC
Registrant Organization
Registrant Street
5335 Gate Parkway care of Network Solutions PO Box 459
Registrant City
Jacksonville
Registrant State/Province
FL
Registrant Postal Code
32256
Registrant Country
US
Registrant Phone
+1.5707088622
Registrant Phone Ext
Registrant Fax
Registrant Fax Ext
Registrant Email
hw7fr4qh2sy@networksolutionsprivateregistration.com
Registry Admin ID
Admin Name
PERFECT PRIVACY, LLC
Admin Organization
Admin Street
5335 Gate Parkway care of Network Solutions PO Box 459
Admin City
Jacksonville
Admin State/Province
FL
Admin Postal Code
32256
Admin Country
US
Admin Phone
+1.5707088622
Admin Phone Ext
Admin Fax
Admin Fax Ext
Admin Email
hw7fr4qh2sy@networksolutionsprivateregistration.com
Registry Tech ID
Tech Name
PERFECT PRIVACY, LLC
Tech Organization
Tech Street
5335 Gate Parkway care of Network Solutions PO Box 459
Tech City
Jacksonville
Tech State/Province
FL
Tech Postal Code
32256
Tech Country
US
Tech Phone
+1.5707088622
Tech Phone Ext
Tech Fax
Tech Fax Ext
Tech Email
dc78b67b8kb@networksolutionsprivateregistration.com
Name Server
NS.EXECULINK.COM
Name Server
NS-BMI.EXECULINK.COM
DNSSEC
unsigned
Registrar Abuse Contact Email
domain.operations@web.com
Registrar Abuse Contact Phone
+1.8777228662
URL of the ICANN WHOIS Data Problem Reporting System
http://wdprs.internic.net/ from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path, system, listdir
import sys
import tty
import termios
import time
import threading

errors = []

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()


def readchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def readkey(getchar_fn=None):
    getchar = getchar_fn or readchar
    c1 = getchar()
    if ord(c1) != 0x1b:
        return c1
    c2 = getchar()
    if ord(c2) != 0x5b:
        return c1
    c3 = getchar()
    return chr(0x10 + ord(c3) - 65)

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
    _thread = threading.Thread(target=working_tip)
    _thread.setDaemon(True)
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

class Modules(object):
    ''' 
        To setup /etc/modules
    '''

    def __init__(self, file="/etc/modules"):
        self.file = file
        with open(self.file, 'r') as f:
            self.configs = f.read()
        self.configs = self.configs.split('\n')

    def remove(self, expected):
        for config in self.configs:
            if expected in config:
                self.configs.remove(config)
        return self.write_file()

    def set(self, name):
        have_excepted = False
        for i in range(len(self.configs)):
            config = self.configs[i]
            if name in config:
                have_excepted = True
                tmp = name
                self.configs[i] = tmp
                break

        if not have_excepted:
            tmp = name
            self.configs.append(tmp)
        return self.write_file()

    def write_file(self):
        try:
            config = '\n'.join(self.configs)
            # print(config)
            with open(self.file, 'w') as f:
                f.write(config)
            return 0, config
        except Exception as e:
            return -1, e

class Config(object):
    ''' 
        To setup /boot/config.txt
    '''

    def __init__(self, file="/boot/config.txt"):
        self.file = file
        with open(self.file, 'r') as f:
            self.configs = f.read()
        self.configs = self.configs.split('\n')

    def remove(self, expected):
        for config in self.configs:
            if expected in config:
                self.configs.remove(config)
        return self.write_file()

    def set(self, name, value=None):
        have_excepted = False
        for i in range(len(self.configs)):
            config = self.configs[i]
            if name in config:
                have_excepted = True
                tmp = name
                if value != None:
                    tmp += '=' + value
                self.configs[i] = tmp
                break

        if not have_excepted:
            tmp = name
            if value != None:
                tmp += '=' + value
            self.configs.append(tmp)
        return self.write_file()

    def write_file(self):
        try:
            config = '\n'.join(self.configs)
            # print(config)
            with open(self.file, 'w') as f:
                f.write(config)
            return 0, config
        except Exception as e:
            return -1, e

def check_raspbain_version():
    _, result = run_command("cat /etc/debian_version|awk -F. '{print $1}'")
    return result.strip()

def install():
    print("Install dependency")
    do(msg="update apt-get",
        cmd='run_command("sudo apt-get update")')
    do(msg="install pip",
        cmd='run_command("sudo apt-get install python3-pip -y")')
    do(msg="install ffmpeg",
        cmd='run_command("sudo apt-get install ffmpeg -y")')
    # do(msg="install setuptools",
    #     cmd='run_command("sudo pip3 install setuptools -y")')

# sudo apt-get install python-rpi.gpio python-spidev python-pip python-pil python-numpy
    do(msg="install git",
        cmd='run_command("sudo apt-get install git-core -y")')
    do(msg="install pi tft dev",
        cmd='run_command("sudo apt-get install python3-rpi.gpio python3-spidev python3-pip python3-pil python3-numpy -y")')

    do(msg="install sysstat",
        cmd='run_command("sudo apt-get install sysstat -y")')
    do(msg="install i2c-tools",
        cmd='run_command("sudo apt-get install i2c-tools -y")')
    do(msg="install httplib2",
        cmd='run_command("sudo pip3 install httplib2")')
    do(msg="install oauth2client",
        cmd='run_command("sudo pip3 install oauth2client")')
    do(msg="install PIL",
        cmd='run_command("sudo pip3 install pillow")')
    do(msg="install smbus",
        cmd='run_command("sudo pip3 install smbus")') 
    do(msg="install spi",
        cmd='run_command("sudo pip3 install Adafruit_GPIO")')
    do(msg="install websockets",
        cmd='run_command("sudo pip3 install websockets")')
    do(msg="install picamera",
        cmd='run_command("sudo apt-get install python3-picamera -y")')
    do(msg="install opencv dev_1",
        cmd='run_command("sudo apt-get install libhdf5-dev libhdf5-serial-dev libhdf5-103 python3-pyqt5 -y")')
    do(msg="install opencv dev_2",
        cmd='run_command("sudo apt-get install libatlas-base-dev libjasper-dev libavcodec-dev libavformat-dev  libswscale-dev -y")')
    do(msg="install opencv-contrib-python",
        cmd='run_command("sudo pip3 install opencv-contrib-python==4.5.3.56")')
    do(msg="install numpy",
        cmd='run_command("sudo pip3 install -U numpy")')
    do(msg="install google-api",
        cmd='run_command("sudo pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib oauth2client")')

    raspbain_version = check_raspbain_version()
    if raspbain_version == "10":
        do(msg="install libopenexr23",
            cmd='run_command("sudo apt-get install libopenexr23 -y")')     
    elif raspbain_version == "11":
        do(msg="install libopenexr25",
            cmd='run_command("sudo apt-get install libopenexr25 -y")') 


    print("Setup interfaces")
    do(msg="turn on I2C",
        cmd='Config().set("dtparam=i2c_arm", "on")') 
    do(msg="Add I2C module",
        cmd='Modules().set("i2c-dev")') 

    do(msg="turn on SPI",
        cmd='Config().set("dtparam=spi", "on")') 
    # do(msg="Add SPI module",
    #     cmd='Modules().set("spi-dev")') 
    do(msg="turn on Camera",
        cmd='Config().set("start_x", "1")') 
    do(msg="turn on Camera",
        cmd='Config().set("gpu_mem", "256")') 

    if "Pictures" not in listdir("/home/pi"):
        do(msg="create .rascam directory",
            cmd='run_command("mkdir /home/pi/Pictures/")')
    if "rascam_picture_file" not in listdir("/home/pi/Pictures"):
        do(msg="create .rascam directory",
            cmd='run_command("mkdir /home/pi/Pictures/rascam_picture_file")')
        do(msg="change directory own",
            cmd='run_command("sudo chown -R pi:pi /home/pi/Pictures/rascam_picture_file/")')   
    if "time_lapse_video" not in listdir("/home/pi/Pictures"):
        do(msg="create time_lapse_video directory",
            cmd='run_command("sudo mkdir /home/pi/Pictures/time_lapse_video")')  
        do(msg="change directory own",
            cmd='run_command("sudo chown -R pi:pi /home/pi/Pictures/time_lapse_video/")')  

    do(msg="copy rascam-config",
        cmd='run_command("sudo cp ./data/config /home/pi/.rascam_config")')
    do(msg="change directory owner",
        cmd='run_command("sudo chown -R pi:pi /home/pi/.rascam_config")')

    # print("Setup rascam web-example service") 
    # do(msg="copy rascam web-example file",
    #     cmd='run_command("sudo cp ./bin/rascam-web-example /etc/init.d/rascam-web-example")')
    # do(msg="add excutable mode for rascam-web-example",
    #     cmd='run_command("sudo chmod +x /etc/init.d/rascam-web-example")')

## install lib software and build dir
install()


from setuptools import setup, find_packages
setup(
    name='rascam',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version="0.0.2",

    description='rascam for Raspberry Pi',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/sunfounder/rascam',

    # Author details
    author='SunFounder',
    author_email='service@sunfounder.com',

    # Choose your license
    license='GNU',
    zip_safe=False,
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],

    # What does your project relate to?
    keywords='camera raspberry pi HQ sunfounder',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['examples', 'tests*']),

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    # install_requires=['RPi.GPIO', 'smbus', 'picamera'],
 
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    # entry_points={
    #     'console_scripts': [
    #         'rascam=rpi_cam.utils:main', 
    #     ],
    # },
)

if len(errors) == 0:
    print("Setup Finished")
    print('If you want to reboot please press y, if not press n')
    input_val = readkey()
    print(input_val)
    if input_val == 'y':
        do(msg="System reboot now",
        cmd='run_command("sudo reboot")')
    elif input_val == 'n':
        print("reboot cancel")
else:
    print("\n\nError happened in install process:")
    for error in errors:
        print(error)
    print("Try to fix it yourself, or contact service@sunfounder.com with this message")
