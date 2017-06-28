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