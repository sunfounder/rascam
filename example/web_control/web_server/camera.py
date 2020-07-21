import numpy as np
import cv2
import io
import threading
from flask import Flask, render_template, Response
from picamera import PiCamera
from picamera.array import PiRGBArray
from multiprocessing import Process, Manager, Queue, Pipe
from datetime import datetime


queue = Queue()

app = Flask(__name__)
@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

def gen():
    """Video streaming generator function."""
    while True:  
        # frame = cv2.imread("123.jpeg")Vilib.q.get()  
        # print("1")
        # if Vilib.conn2.recv()
        # frame = cv2.imencode('.jpg', Vilib.conn2.recv())[1].tobytes() 
        # rt_img = np.ones((320,240),np.uint8)
        # print("2")
        # Vilib.frame = cv2.imencode('.jpg', Vilib.img_array[0])[1].tobytes()
        # print(Vilib.img_array[0].shape)
        frame = cv2.imencode('.jpg', Vilib.img_array)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        

@app.route('/mjpg')
def video_feed():
    # from camera import Camera
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame') 

def web_camera_start():
    app.run(host='0.0.0.0', port=8888,threaded=True)

class Vilib(object): 
    
    # cam = PiCamera()
    # img_array = Manager().list()
    # rt_img = np.ones((320,240),np.uint8)
    # img_array = rt_img
    # conn1,conn2 = Pipe()
    # take_flag = False
    filename = ''
    img_array = []
    
    @staticmethod
    def camera_clone():
        Vilib.cam = PiCamera()
        Vilib.cam.resolution = (480, 640)
        rawCapture = PiRGBArray(Vilib.cam, size=Vilib.cam.resolution)
        # stream = io.BytesIO()
        while True:
            for frame in Vilib.cam.capture_continuous(rawCapture, format="bgr", use_video_port=True):
                img = frame.array
                # print(img.shape)
                # img = cv2.utils.dumpInputArray(img)
                # print(img)
                Vilib.img_array = img
                # Vilib.conn1.send(img)
                # queue.put(img)
                # print(Vilib.img_array)
                rawCapture.truncate(0)
                # if Vilib.   == True:
                #     cam.stop()

    @staticmethod
    def run_command(cmd=""):
        import subprocess
        p = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        result = p.stdout.read().decode('utf-8')
        status = p.poll()
        # print(result)
        # print(status)
        return status, result
    @staticmethod
    def snapstart(): # take pictures on demand
        # Vilib.take_flag = True
        # Vilib.worker_2.terminate()
        # Vilib.worker_2.join()
        # camera = PiCamera()
        # camera.resolution = (375,535)
        print('take a pictrue')
        t='{:%Y%m%d-%H%M%S}'.format(datetime.now())
        Vilib.filename = t+'.jpg'
        Vilib.cam.capture(Vilib.filename)
        # Vilib.take_flag = False
        # Vilib.worker_2 = Process(name='worker 2',target=Vilib.camera_clone)
        # Vilib.worker_2.start()
        Vilib.run_command(cmd="cp ./{} /home/pi/rascam/web_control/web_client/image/temp.jpg".format(Vilib.filename))
        Vilib.run_command(cmd="mv ./{} /home/pi/Pictures/rascam_picture_file".format(Vilib.filename))
        

    @staticmethod
    def camera_start():
        # from multiprocessing import Process
        
        # Vilib.worker_2 = Process(name='worker 2',target=Vilib.camera_clone)
        # worker_1 = Process(name='worker 1',target=web_camera_start)
        # worker_1.start()
        # # print("hahahahhah")
        # Vilib.worker_2.start()
        # print("hehehhehehhe")
        t2 = threading.Thread(target=web_camera_start)
        t2.start()
        t1 = threading.Thread(target=Vilib.camera_clone)
        t1.start()
    
# Vilib.camera_start()
    
    
    