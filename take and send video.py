from picamera import PiCamera
import subprocess
from twython import Twython
from keys import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

camera = PiCamera()
camera.rotation = 180
twitter = Twython(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

camera.start_preview()
camera.start_recording('/home/pi/Desktop/helenvideo.h264')
camera.wait_recording(3)
camera.stop_recording()
camera.stop_preview()

cp = subprocess.run(["rm /home/pi/Desktop/helenvideo.mp4"],shell=True)
cp = subprocess.run(["MP4Box -add /home/pi/Desktop/helenvideo.h264 /home/pi/Desktop/helenvideo.mp4"],shell=True)

video = open('/home/pi/Desktop/helenvideo.mp4', 'rb')
response = twitter.upload_video(media=video, media_type='video/mp4')
twitter.update_status(status='trying automated h264 to mp4 conversion with another subprocess', media_ids=[response['media_id']])