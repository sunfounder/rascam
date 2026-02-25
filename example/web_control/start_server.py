import os
import cv2
import threading
import time
from flask import Flask, render_template, Response, jsonify
from picamera2 import Picamera2
from datetime import datetime
import google_upload as google

# System Environment Configuration
USERNAME = os.popen('id -un 1000').read().strip()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Flask Application Setup
# Static and template folders are mapped to the current directory
app = Flask(__name__, 
            template_folder=os.path.normpath(BASE_DIR), 
            static_folder=os.path.normpath(BASE_DIR), 
            static_url_path='')

class Vilib:
    """Camera management and image processing class."""
    img_array = None
    filename = ""
    _should_snap = False
    
    @staticmethod
    def camera_loop():
        """Main thread for camera capture and hardware control."""
        cam = Picamera2()
        config = cam.create_preview_configuration(main={"size": (640, 480), "format": "RGB888"})
        cam.configure(config)
        cam.start()
        print("Hardware initialized: Camera is running.")

        while True:
            try:
                # Capture frame from hardware
                raw_frame = cam.capture_array()
                
                # Update shared frame buffer
                # Note: No color conversion is applied as the raw stream matches display requirements
                Vilib.img_array = raw_frame

                # Snapshot Trigger Logic
                if Vilib._should_snap:
                    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
                    Vilib.filename = f"{timestamp}.jpg"
                    
                    # 1. Save high-resolution archive to the user's Pictures folder
                    backup_dir = f"/home/{USERNAME}/Pictures/rascam_picture_file"
                    os.makedirs(backup_dir, exist_ok=True)
                    cv2.imwrite(os.path.join(backup_dir, Vilib.filename), Vilib.img_array)
                    
                    # 2. Save temporary copy for web preview
                    temp_path = os.path.join(BASE_DIR, "image", "temp.jpg")
                    os.makedirs(os.path.dirname(temp_path), exist_ok=True)
                    cv2.imwrite(temp_path, Vilib.img_array)
                    
                    print(f"File saved successfully: {Vilib.filename}")
                    Vilib._should_snap = False
            
            except Exception as e:
                print(f"Camera Loop Error: {e}")
            
            time.sleep(0.01)

# --- Flask Routes ---

@app.route('/')
def index():
    """Render the main control interface."""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """MJPEG video streaming endpoint for real-time preview."""
    def gen():
        while True:
            if Vilib.img_array is not None:
                success, jpeg = cv2.imencode('.jpg', Vilib.img_array)
                if success:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
            time.sleep(0.04) # Target ~25 FPS
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/take_picture')
def take_picture():
    """Trigger a snapshot and wait for file synchronization."""
    Vilib._should_snap = True
    
    # Wait for the camera thread to finish writing the file (max 2 seconds)
    timeout = 2.0
    start_time = time.time()
    while Vilib._should_snap and (time.time() - start_time < timeout):
        time.sleep(0.1)
        
    return jsonify({
        "status": "ok", 
        "url": "/image/temp.jpg?t=" + str(int(time.time())) # Append timestamp to bypass browser cache
    })

@app.route('/share')
def share():
    """Upload the most recent photo to Google Drive via external API."""
    try:
        file_path = f"/home/{USERNAME}/Pictures/rascam_picture_file"
        upload_result = google.upload(file_path=file_path, file_name=Vilib.filename)
        
        if upload_result == Vilib.filename:
            return jsonify({"status": "success"})
        return jsonify({"status": "failed"})
    
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)})

if __name__ == '__main__':
    # Initialize hardware capture in a background daemon thread
    threading.Thread(target=Vilib.camera_loop, daemon=True).start()
    
    # Start Web Server
    # host='0.0.0.0' allows access from other devices on the same network
    app.run(host='0.0.0.0', port=8888, threaded=True)