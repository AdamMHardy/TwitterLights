import sys
import os
from time import sleep
import wiringpi
from twython import TwythonStreamer
import threading

# Search terms
TERMS = '#merrychristmas'
LED = 1 #For use with WiringPi - Board pin 12, BCM 18

# Twitter application authentication
API_KEY = '<Consumer API Key>'
API_SECRET = '<Consumer API Secret Key>'
ACCESS_TOKEN = '<OAuth Access Token>'
ACCESS_TOKEN_SECRET = '<OAuth Access Token Secret>'

# WiringPi setup
wiringpi.wiringPiSetup()
wiringpi.pinMode(LED, 1)
wiringpi.softPwmCreate(LED,0,100)
wiringpi.softPwmWrite(LED,100)
brightness = 100

# Setup twitter stream callbacks for PWM-driven Lights
class TwitterLightsStreamer(TwythonStreamer):
        def __init__(self, api_key, api_secret, access_token, access_token_secret, lightControl):
                TwythonStreamer.__init__(self, api_key, api_secret, access_token, access_token_secret)
                self.lightControl = lightControl
                lightControl.tick()
        def on_success(self,data):
                if 'text' in data:
                        print data['text'].encode('utf-8')
                        print
                        self.lightControl.bumpPower()
        def on_error(self, status_code, data):
                print(status_code)

# Setup Light Control
class lightControl():
        def __init__(self, brightness):
                self.power = brightness

        def printPower(self):
                print(self.power)

        def bumpPower(self):
                self.power = 100
                self.updateDutyCycle()
        def updateDutyCycle(self):
                if self.power > 10:
                        wiringpi.softPwmWrite(LED,self.power)

        def drainPower(self):
                self.power = self.power -1 if self.power > 10 else self.power

        def tick(self):
                timer = threading.Timer(0.01, self.tock)
                timer.start()

        def tock(self):
                self.drainPower()
                self.updateDutyCycle()
                self.tick()

# Create Light Control and Streamer
lightControl = lightControl(brightness)
stream = TwitterLightsStreamer(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, lightControl)

running = True

while running:
        try:
                print('Starting')
                stream.statuses.filter(track=TERMS)
        except (KeyboardInterrupt, SystemExit):
                print('Exiting')
                print('Stopping Lights')
                wiringpi.softPwmWrite(LED, 0)
                running = False
                print('Hit Ctrl+c again to exit')
                sys.exit(0)
        except:
                print('error')
