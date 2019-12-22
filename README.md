#  TwitterLights

## Description

I was looking for a cool project over the holidays and since my wife found some new Christmas lights for our mantel, I figured I'd do something with those.  This project uses Twitter stream code from Twython to increase brightness of the lights each time a tweet with a specified hashtag is tweeted - I used #merrychristmas.

Everytime someone tweets with #MerryChristmas, these lights increase to 100% brightness and then drain down to 10% until a new tweet is sent.

![Lights in action]()
Note: Flickering in the video is due to camera refresh rate

This project is based off of [this one](https://github.com/third774/twitter-christmas), but I've modified it to use WiringPi instead of RPi.GPIO for a less jittery PWM on the PI Zero.
## Requirements

1. Raspberry Pi - I used a Zero W
2. Switching Transistor - 2N2222 (or similar - MOSFETS work too)
3. 470 Ohm Resistor - between the Raspberry Pin and Base of the transistor
4. DC powered light strip - We got ours at target, they are battery powered which makes it very easy to connect to the Pi

## Installation

### Hardware Setup
I checked the amperage of the light strand at 5v and it came in just over 4mA.  Since this is within the safe range of current that can be drawn from the Raspberry Pi directly, I decided not to use a separate external power source for the lights.

Pins used on the Raspberry Pi
`pin 2 - +5v`
`pin 6 - GROUND`
`pin 12 - PWM Output, BCM18`

Connect:
- +5v (pin 2) to the positive side of your light strand
- The negative/ground side of your light strand to the Collector of your 2n2222
- Transistor Emitter connects to GROUND (pin 6)
- PWM Output (pin 12) to 470 Ohm resistor to transistor Base

### Software Setup
Start by installing your preferred flavor of OS on the Raspberry Pi.  I installed Raspbian Buster Lite. It has most of what I need and I just run it in headless mode.  Makesure everything is up-to-date by running: `sudo apt-get update && sudo apt-get upgrade`

Ensure you have Python installed, I'm using an older version - 2.7.16, but it works. You can check if python is installed by checking the version: `python --version`

Install [pip](https://pip.pypa.io/en/stable/reference/pip_install/) - this is the easiest way to install the next dependancies. pip is installed by default in Raspbian Desktop images (but not Raspbian Lite). You can install it with apt:

`sudo apt install python3-pip`

To get the Python 2 version:

`sudo apt install python-pip`

pip3 installs modules for Python 3, and pip installs modules for Python 2.

Install [Twython](https://twython.readthedocs.io/en/latest/) - This is a great Twitter API wrapper for Python, we will use it to monitor the the stream api for new tweets.

`pip install twython`

We'll use [WiringPi](http://wiringpi.com) to handle the PWM output to the lights. It comes preinstalled on all Raspbian systems but you can install it using this command if you need.

`sudo apt-get install wiringpi`

Log into the Twitter Developer site and create a new App to get the OAuth Credentails.

Copy the contents of the TwitterLights.py file to your Pi and update the Twitter Application Authentication section with your details.

You can change the `TERMS` definition to monitor any other hashtag

### Run It
Start up the lights!
`sudo python TwitterLights.py`

Use `ctl+c` to exit

## Credits
- https://github.com/third774/twitter-christmas - This is where I found the code that inspired this project
- https://learn.sparkfun.com/tutorials/raspberry-pi-twitter-monitor/all







