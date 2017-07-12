import picamera
import time
import sys
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-l", "--vidlen", help="Length of the video recording (secs)")
ap.add_argument("-o", "--outfile", help="Filename without the extension")
ap.add_argument("-f", "--format", help="Format (mjpeg or h264")
args = vars(ap.parse_args())
    
camera = picamera.PiCamera()
camera.resolution = (1296, 972)
camera.contrast = 100
camera.brightness = 75
camera.framerate = 25
camera.exposure_mode = 'auto'
camera.awb_mode = 'off'
camera.awb_gains = (1.8, 1.0)
camera.led = False
camera.rotation = 180

if args["format"] == 'h264':
    camera.start_recording(args["filename"] + '.h264', format="h264")
elif args["format"] == 'mjpeg':
    camera.start_recording(args["filename"] + '.mjpeg', format='mjpeg')
else:
    print 'ERROR> Invalid format specified, must be h264 or mjpeg'
    print 'Exiting...'
    sys.exit(1)
    
#TODO: Replace sleep with more accurate timer
time.sleep(args["vidlen"])

camera.stop_recording()

sys.exit()
