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
import json
import types

def parse_json():
    if os.path.exists('trial_config.json'):
        with open(os.path.join('trial_config.json'), 'r') as jsonFile:
            jsonString = jsonFile.read()
            paramsDict = json.loads(jsonString)
            for k,v in paramsDict.iteritems():
                if type(v) == types.UnicodeType:
                    path_elems = v.split('\\')
                    newPath = os.path.join(*path_elems)
                    paramsDict[k] = newPath
        config_dict = paramsDict

        # check error conditions
        if config_dict is None:
            print 'Error> Config dictionary is None, problem parsing config.json'

        return config_dict
    else:
        print 'Error> No config.json, will use hard-coded defaults'
        return None

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
        print 'videoCapture(): Initializing Camera...'
        camera = picamera.PiCamera()
        camera.resolution = (1296, 972)
        camera.contrast = 100
        camera.brightness = 85
        camera.framerate = 25
        camera.exposure_mode = 'auto'
        camera.awb_mode = 'off'
        camera.awb_gains = (2.8, 1.0)
	camera.saturation = -20
        camera.led = False
        camera.rotation = 180

        print 'videoCapture(): Starting Recording...'
        camera.start_recording(vidOut, format='h264')

    print 'videoCapture(): Sleep ' + str(vidLength) + ' secs (video duration)...'
    currenttime = datetime.datetime.now()
    finaltime = currenttime + datetime.timedelta(seconds=vidLength)
    while datetime.datetime.now() < finaltime:
        # TODO: Need to figure out why 'continue' doesn't work here?!?!?
        time.sleep(0.1)

    if useCamera:
        print 'videoCapture(): Stopping Recording...'
        camera.stop_recording()
        print 'videoCapture(): Closing Camera...'
        camera.close()

    captureDone = True

class Trial:

    global captureDone

    def __init__(self, stim, starttime, cwtime, ccwtime, fedside, startDelay):

        self.vidout = None
        self.stimulus = stim
        self.start = starttime
        self.cwtime = 0.8
	self.ccwtime = 0.8
	# self.cwtime = float(cwtime)
        # self.ccwtime = float(ccwtime)

        # in our jenkins automation, we need to allow some time for git
        # especially if it has to clone to do its thing and then time sync
        # everything
        self.startDelay = int(startDelay) #seconds (3 minutes)

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

    def videoFileName(self, species, tround, sl, sex, fishid, day, session,
                    thatpistimulus, proportion, fedside, correctside):
        self.vidout = ((str(species) + '_' + str(tround)
                       + '_' + str(sl) + '_' + str(sex) + '_' + str(fishid) + '_' + str(day) + '_' +
                       str(session) + '_' + str(self.stim) + '_' + str(thatpistimulus) + '_' +
                       str(proportion) + '_' + str(fedside) + '_' + str(correctside) + '.h264'))
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

    def runSingleTrial(self, feed, use_camera, sync, feed_dur_secs):

        global captureDone
        captureDone = False

        now = datetime.datetime.now()
        print 'now= ' + str(now)

        #######################################################################
        # if start time is too far in the past then error/exit
        #######################################################################
        if sync:
            # create datetime object with hours/minutes from self.start
            hour, minute = self.start.split(":")
            starttime = now.replace(hour=int(hour))
            starttime = starttime.replace(minute=int(minute))

            # subtract the datetime objects
            time_delta = now - starttime

            # split time delta into mins/secs differences
            mins_delta, secs_delta = divmod(time_delta.days * 86400 + time_delta.seconds, 60)
            print 'mins_delta=' + str(mins_delta)
            print 'secs_delta=' + str(secs_delta)

            # if more than 60 mins then error/exit
            if mins_delta > START_MAX_MINS_IN_PAST:
                print 'ERROR>' + str(self.start) + ' is too far in the past, must be within ' + str(START_MAX_MINS_IN_PAST) + ' mins!'
                print 'Exiting...'
                sys.exit(1)

            time2start = starttime + datetime.timedelta(seconds=self.startDelay)
            print 'time2start= ' + str(time2start)

            # Wait for start time
            print 'Waiting for time2start...'
            while datetime.datetime.now() < time2start:
                pass

        print "(real)starttime= " + str(datetime.datetime.now())

        # Note time that trial really starts
        self.startT = time.time()

        # Start up thread which control the video capture
        thread = Thread(target = videoCapture, args = (TRIAL_DURATION_SECS, self.vidout, use_camera, ))
        thread.start()

        # Sleep a few seconds to allow camera to come up
        time.sleep(SLEEP_AFTER_CAMERA_START_SECS)

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

        print 'Sleeping ' + str(FEED_DELAY_SECS) + ' secs before feeding...'
        time.sleep(FEED_DELAY_SECS)

        # Turn feeders on
        if self.fedside != 'none':
            self.turnOnFeeder(self)

        # Wait for feeder to turn into place time
        print 'Sleep ' + str(intime) + ' secs for feeder to lower...'
        time.sleep(intime)

        # Turn feeders off
        self.turnOffFeeder(self)

        # Wait for feed duration
        print 'Eat Fish, EAT!'
        print 'Sleep ' + str(feed_dur_secs) + ' secs for feeding duration...'
        time.sleep(feed_dur_secs)

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
        print 'Sleep ' + str(outtime) + ' secs to raise feeder out...'
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

    # Defaults
    use_camera = False
    feed = False
    video_file = 'N/A'
    global SLEEP_AFTER_CAMERA_START_SECS
    SLEEP_AFTER_CAMERA_START_SECS = 30
    global FEED_DELAY_SECS
    FEED_DELAY_SECS = 8
    global TRIAL_DURATION_SECS
    TRIAL_DURATION_SECS = 245
    global START_MAX_MINS_IN_PAST
    START_MAX_MINS_IN_PAST = 60
    FEED_DURATION_SECS = 10
    FEED_DURATION_SECS_HABITUATION = 10

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
    ap.add_argument("-m", "--startTime", help="time since epoch that you want to start your trial")
    ap.add_argument("-sd", "--startDelay", help="Number of seconds to delay start (for jenkins this should be 180), NA if sync is false")
    ap.add_argument("-sync", "--dosync", help="do you want to attempt to time sync using startTime and startDelay?", action="store_true")
    args = vars(ap.parse_args())


    config_json = parse_json()
    if config_json is not None:
        if 'SLEEP_AFTER_CAMERA_START_SECS' in config_json:
            SLEEP_AFTER_CAMERA_START_SECS = int(config_json['SLEEP_AFTER_CAMERA_START_SECS'])
        if 'FEED_DURATION_SECS' in config_json:
            FEED_DURATION_SECS = int(config_json['FEED_DURATION_SECS'])
        if 'FEED_DURATION_SECS_HABITUATION' in config_json:
            FEED_DURATION_SECS_HABITUATION = int(config_json['FEED_DURATION_SECS_HABITUATION'])
        if 'FEED_DELAY_SECS' in config_json:
            FEED_DELAY_SECS = int(config_json['FEED_DELAY_SECS'])
        if 'TRIAL_DURATION_SECS' in config_json:
            TRIAL_DURATION_SECS = int(config_json['TRIAL_DURATION_SECS'])
        if 'START_MAX_MINS_IN_PAST' in config_json:
            START_MAX_MINS_IN_PAST = int(config_json['START_MAX_MINS_IN_PAST'])

    # Feed duration is longer during habituation, then shortens drastically
    if int(args["day"]) < 3:
        feed_dur = FEED_DURATION_SECS_HABITUATION
    else:
        feed_dur = FEED_DURATION_SECS

    T = Trial(args["pistimulus"], args["startTime"], args["cwtime"], args["ccwtime"], args["fedside"], args["startDelay"])

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
    T.runSingleTrial(feed, use_camera, args['dosync'], feed_dur)

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
