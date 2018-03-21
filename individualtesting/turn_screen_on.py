import os
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
ap.add_argument("-l", "--len", help="How long do you want the screen on (secs)")
ap.add_argument("-i", "--image", help="Image to show on screen")
args = vars(ap.parse_args())

# send export DISPLAY=:0.0 (this is linux specific)
os.environ["DISPLAY"] = ":0.0"

global captureDone
captureDone = False

# Start up thread that turns on display
thread = Thread(target = displayImage, args = (args["image"],))
thread.start()

# Wait desired time
#TODO: Replace sleep with more accurate timer
time.sleep(float(args["len"]))

# Signal other thread to turn off screen
captureDone = True

# Give it a second
time.sleep(1)

# Done, join threads back to thread pool
print 'Done'
thread.join()

pygame.quit()

sys.exit()
