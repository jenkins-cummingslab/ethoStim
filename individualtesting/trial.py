#! /usr/python

'''
///////////////////////////////////////////////////////////
//  Permission is hereby granted, free of charge,
//  to any person obtaining a copy of
//  this software and associated documentation files
//  (the "Software"), to deal in the Software without
//  restriction, including without limitation the rights
//  to use, copy, modify, merge, publish, distribute,
//  sublicense, and/or sell copies of the Software, and
//  to permit persons to whom the Software is furnished

//  to do so, subject to the following conditions:
//
//  The above copyright notice and this permission notice
//  shall be included in all copies or substantial portions
//  of the Software.
//
//  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF
//  ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
//  TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
//  PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
//  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
//  CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
//  OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
//  IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
//  DEALINGS IN THE SOFTWARE.
'''

__author__ = 'RobertIan'
__version__ = '0.1.1'

import argparse
import pygame
import picamera
import time
import datetime
import netifaces
import RPi.GPIO as GPIO
import sys
import os
from threading import Thread

def getIpAddr():
   ip = netifaces.ifaddresses('eth0')[2][0]['addr']
   print ip
   return ip

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

def videoCapture(vidLength, vidOut, useCamera):
    global captureDone

    if useCamera:
        print 'Initializing Camera...'
        camera = picamera.PiCamera()
        camera.resolution = (1280, 720)
        camera.contrast = 100
        camera.brightness = 75
        camera.framerate = 25
        camera.exposure_mode = 'auto'
        camera.awb_mode = 'off'
        camera.awb_gains = (1.8, 1.0)
        camera.led = False
        camera.rotation = 180

        print 'Starting Recording...'
        camera.start_recording(vidOut, format='h264')

    print 'Sleep ' + str(vidLength) + ' secs...'
    currenttime = datetime.datetime.now()
    finaltime = currenttime + datetime.timedelta(seconds=vidLength)
    while datetime.datetime.now() < finaltime:
        time.sleep(0.1)

    if useCamera:
        print 'Stopping Recording...'
        camera.stop_recording()
        print 'Closing Camera...'
        camera.close()

    captureDone = True

class Trial:

    global captureDone

    def __init__(self, stim, starttime, cwtime, ccwtime, fedside):

        self.vidout = None
        self.stimulus = stim
        self.start = starttime
        self.tLength = 245 #seconds
        self.feedDelay = 8 #seconds
        self.feedDuration = 220 #seconds
        #self.cwtime = float(cwtime) #seconds
        #self.ccwtime = float(ccwtime) #seconds
        self.cwtime = .65 #seconds
        self.ccwtime = .65 #seconds
        self.startDelay = 3 #minutes

        self.feeder_en = 17
        self.feeder_a = 27
        self.feeder_b = 22
        #self.freq = 100
        #self.dc = 13
        self.feeder = None
        self.ip = None
        self.fedside = fedside

        # Configure RPi GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.feeder_en, GPIO.OUT)
        GPIO.setup(self.feeder_a, GPIO.OUT)
        GPIO.setup(self.feeder_b, GPIO.OUT)
        GPIO.output(self.feeder_en, 0)
        GPIO.output(self.feeder_a, 0)
        GPIO.output(self.feeder_b, 0)
        print "GPIOinit"

    def whatStimulus(self):
        self.stim, extension = os.path.splitext(self.stimulus)

    # Sets Feeder(s) direction to clockwise
    @staticmethod
    def setFeederDirCw(self):
        GPIO.output(self.feeder_a, 1)
        GPIO.output(self.feeder_b, 0)
        print 'setFeederDirCw'

    # Sets Feeder(s) direction to counter clockwise
    @staticmethod
    def setFeederDirCcw(self):
        GPIO.output(self.feeder_a, 0)
        GPIO.output(self.feeder_b, 1)
        print 'setFeederDirCcw'

    @staticmethod
    def turnOnFeeder(self):
        #self.p = GPIO.PWM(self.feeder_en, self.freq)
        #self.p.start(self.dc)
        GPIO.output(self.feeder_en, 1)
        print 'turnOnFeeder'

    @staticmethod
    def turnOffFeeder(self):
        #self.p.stop()
        GPIO.output(self.feeder_en, 0)
        print 'turnOffFeeder'

    @staticmethod
    def cameraInit(self):
        self.camera = picamera.PiCamera()
        self.camera.resolution = (1280, 720)
        self.camera.contrast = 100
        self.camera.brightness = 75
        self.camera.framerate = 25
        self.camera.exposure_mode = 'auto'
        self.camera.awb_mode = 'off'
        self.camera.awb_gains = (1.8, 1.0)
        self.camera.led = False
        presented = False
        self.camera.rotation = 180
        # self.camera.iso = 800

    def videoFileName(self, species, tround, sl, sex, fishid, day, session,
                    thatpistimulus, proportion, fedside, correctside):
        self.vidout = ((str(species) + '_' + str(tround)
                       + '_' + str(sl) + '_' + str(sex) + '_' + str(fishid) + '_' + str(day) + '_' +
                       str(session) + '_' + str(self.stim) + '_' + str(thatpistimulus) + '_' +
                       str(proportion) + '_' + str(fedside) + '_' + str(correctside) + '.mkv'))
        print self.vidout
        return self.vidout

    @staticmethod
    def startRecording(self):
        self.camera.start_recording(self.vidout, format='h264')

    @staticmethod
    def stopRecording(self):
        self.camera.stop_recording()

    @staticmethod
    def cameraQuit(self):
        self.camera.close()

    def safeQuit(self):
        # Ensure feeders are OFF
        self.turnOffFeeder(self)
        GPIO.output(self.feeder_en, 0)
        GPIO.output(self.feeder_a, 0)
        GPIO.output(self.feeder_b, 0)
        GPIO.cleanup()
        print "GPIOcleanup"
        pygame.quit()
        sys.exit()

    def runSingleTrial(self, feed, use_camera):

        global captureDone
        captureDone = False

        now = datetime.datetime.now()
        print 'now= ' + str(now)

        hour, minute = self.start.split(":")
        new_minute = float(minute) + self.startDelay

        time2start = now.replace(hour=int(hour))
        time2start = time2start.replace(minute=int(new_minute))
        time2start = time2start.replace(second=0)
        time2start = time2start.replace(microsecond=0)

        print 'time2start= ' + str(time2start)

        # Wait for start time
        while datetime.datetime.now() < time2start:
            pass

        print "(real)starttime= " + str(datetime.datetime.now())

        # Note time that trial really starts
        self.startT = time.time()

        # Start up thread which control the video capture
        thread = Thread(target = videoCapture, args = (self.tLength, self.vidout, use_camera, ))
        thread.start()

        # Sleep a few seconds to allow camera to come up
        time.sleep(2)

        # Turn on display
        thread2 = Thread(target = displayImage, args = (self.stimulus,))
        thread2.start()

        if feed:
            # Set feeders direction to clockwise
            self.setFeederDirCw(self)
            intime = self.cwtime
            outtime = self.ccwtime
        else:
            # Set feeders direction to counter clockwise
            self.setFeederDirCcw(self)
            intime = self.ccwtime
            outtime = self.cwtime

        time.sleep(self.feedDelay)

        # Turn feeders on
        if self.fedside != 'none':
            self.turnOnFeeder(self)
        # Wait for feeder to turn into place time
        print 'Sleep ' + str(intime) + ' secs'
        time.sleep(intime)
        # Turn feeders off
        self.turnOffFeeder(self)
        # Wait for feed duration
        print 'Eat Fish, EAT!'
        print 'Sleep ' + str(self.feedDuration) + ' secs'
        time.sleep(self.feedDuration)
        # Switch direction
        if feed:
            # Set feeders direction to counter clockwise
            self.setFeederDirCcw(self)
        else:
            # Set feeders direction to clockwise
            self.setFeederDirCw(self)
        # Turn feeders on
        if self.fedside != 'none':
            self.turnOnFeeder(self)
        # Return to start position
        print 'Sleep ' + str(outtime) + ' secs'
        time.sleep(outtime)
        # Turn feeders off
        self.turnOffFeeder(self)

        print 'Wait for recording to complete'
        while not captureDone:
	    time.sleep(1)
            print 'Waiting...'

        print 'Done'
        thread.join()
        thread2.join()

if __name__ == '__main__':

    use_camera = False
    feed = False
    video_file = 'N/A'

    # send export DISPLAY=:0.0 (this is linux specific)
    os.environ["DISPLAY"] = ":0.0"

    ap = argparse.ArgumentParser()
    ap.add_argument("-a", "--cwtime", help="Time is seconds that motor(s) is on in clockwise dir")
    ap.add_argument("-b", "--ccwtime", help="Time is seconds that motor(s) is on in counter clockwise dir")
    ap.add_argument("-f", "--fish", help="ID of fish in tank")
    ap.add_argument("-ts", "--thatpistimulus", help="numerosity stimulus being shown on the other raspberry pi in the tank")
    ap.add_argument("-ps", "--pistimulus", help="stimulus being presented with this raspberry pi")
    ap.add_argument("-cs", "--correctside", help="stimulus side on which the correct stimulus is being presented")
    ap.add_argument("-d", "--day", help="experiment day, e.g. 1-7")
    ap.add_argument("-s", "--session", help="trial session, e.g. 1-4")
    ap.add_argument("-fs", "--fedside", help="side feed on/conditioned side")
    ap.add_argument("-x", "--sex", help="fish sex")
    ap.add_argument("-p", "--proportion", help="ratio that is being presented this trial")
    ap.add_argument("-sp", "--species", help="species name")
    ap.add_argument("-sl", "--fishstandardlength", help="standard length of the")
    ap.add_argument("-r", "--round", help="training round")
    ap.add_argument("-fd", "--feed", help="feed with this stimulus", action="store_true")
    ap.add_argument("-c", "--camera", help="do you want to record using this pi?", action="store_true")
    ap.add_argument("-m:", "--startTime", help="time since epoch that you want to start your trial")
    args = vars(ap.parse_args())


    T = Trial(args["pistimulus"], args["startTime"], args["cwtime"], args["ccwtime"], args["fedside"])

    T.ip = getIpAddr()
    T.whatStimulus()

    # Set video filename
    video_file = T.videoFileName(args["species"], args["round"], args["fishstandardlength"],
                    args["sex"], args["fish"], args["day"], args["session"], args["thatpistimulus"], args["proportion"], args["fedside"], args["correctside"])

    # Determine if camera will be used
    if args["camera"]:
        use_camera = True

    # Determine if feeding is needed
    if args["feed"]:
        feed = True

    # Display image, record video, and feed (for those that
    # are applicable)
    T.runSingleTrial(feed, use_camera)

    # Write video file name out to temp.txt, needed by Jenkins
    # only applicable if camera is in use, this needs to be done
    # after the trial has been run to keep time sync
    if args["camera"]:
        f = open("temp.txt", "w")
        f.write(video_file)
        f.close()

    # Cleanup and Exit
    T.safeQuit()
    print "safequit"
