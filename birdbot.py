from picamera import PiCamera
import picamera.array
import numpy as np
import subprocess
from twython import Twython
from keys import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

class DetectMotion(picamera.array.PiMotionAnalysis):
    def __init__(self, camera, size=None):
        super(DetectMotion, self).__init__(camera, size)
        self.motionDetected = False
    def analyze(self, a):
        a = np.sqrt(
            np.square(a['x'].astype(np.float)) +
            np.square(a['y'].astype(np.float))
            ).clip(0, 255).astype(np.uint8)
        if (a > 80).sum() > 10:
            print("h")
            self.motionDetected = True

twitter = Twython(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

while True:
    with picamera.PiCamera() as camera:
        with DetectMotion(camera) as output:
            camera.resolution = (640, 480)
            camera.rotation = 180
            camera.start_recording('/home/pi/Desktop/isitabirdvideo.h264', format='h264', motion_output=output)
            camera.wait_recording(15)
            camera.stop_recording()
            if output.motionDetected == True:
                print("potential bird detected")                
                cp = subprocess.run(["rm /home/pi/Desktop/isitabirdvideo.mp4"],shell=True)
                cp = subprocess.run(["MP4Box -add /home/pi/Desktop/isitabirdvideo.h264 /home/pi/Desktop/isitabirdvideo.mp4"],shell=True)
                video = open('/home/pi/Desktop/isitabirdvideo.mp4', 'rb')
                response = twitter.upload_video(media=video, media_type='video/mp4')
                twitter.update_status(status='Birdbot activated: is this a bird? Do you know what type?', media_ids=[response['media_id']])                
            if output.motionDetected == False:
                print("no potential bird detected")