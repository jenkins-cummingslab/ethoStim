import os
import picamera
import time
import sys
import argparse
import pygame
from threading import Thread

def displayImage(stimulus):
 global captureDone

 pygame.display.init()
 pygame.mouse.set_visible(False)
 screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

 stim, extension = os.path.splitext(stimulus)
 if extension == '.png' or extension == '.PNG' or extension == '.jpg' or extension == '.JPG':
 # still image
     try:
         image = pygame.image.load('src/' + str(stimulus))
         image = pygame.transform.scale(image, (640, 460))
     except IOError:
         print 'Are you sure this file exists? check the src folder \
         ony jpg/JPG, png/PNG formats'

 while not captureDone:
     pygame.display.flip()
     screen.blit(image, (40, 0))

ap = argparse.ArgumentParser()
ap.add_argument("-l", "--vidlen", help="Length of the video recording (secs)")
ap.add_argument("-i", "--image", help="Image to show on screen")
ap.add_argument("-o", "--outfile", help="Filename without the extension")
ap.add_argument("-f", "--format", help="Format (mjpeg or h264")
args = vars(ap.parse_args())

# send export DISPLAY=:0.0 (this is linux specific)
os.environ["DISPLAY"] = ":0.0"

global captureDone
captureDone = False

# Start up thread that turns on display
thread = Thread(target = displayImage, args = (args["image"],))
thread.start()

# Set up camera
camera = picamera.PiCamera()
camera.resolution = (1296, 972)
camera.contrast = 100
camera.brightness = 85
camera.framerate = 25
camera.exposure_mode = 'auto'
camera.awb_mode = 'off'
camera.awb_gains = (2.8, 1.0)
camera.led = False
camera.rotation = 180

# Start recording
if args["format"] == 'h264':
    camera.start_recording(args["outfile"] + '.h264', format="h264")
elif args["format"] == 'mjpeg':
    camera.start_recording(args["outfile"] + '.mjpeg', format='mjpeg')
else:
    print 'ERROR> Invalid format specified, must be h264 or mjpeg'
    print 'Exiting...'
    sys.exit(1)

# Wait desired time
#TODO: Replace sleep with more accurate timer
time.sleep(float(args["vidlen"]))

# Stop recording
camera.stop_recording()

# Signal other thread to turn off screen
captureDone = True

# Give it a second
time.sleep(1)

# Done, join threads back to thread pool
print 'Done'
thread.join()

sys.exit()
