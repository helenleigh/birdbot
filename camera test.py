from picamera import PiCamera
camera = PiCamera()
camera.rotation = 180

camera.start_preview()
camera.start_recording('/home/pi/Desktop/testvideo.h264')
camera.wait_recording(3)
camera.stop_recording()
camera.stop_preview()