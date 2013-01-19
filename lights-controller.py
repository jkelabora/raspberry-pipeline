import time
from time import sleep
import re
import beanstalkc
from LPD8806 import *

beanstalk = beanstalkc.Connection(host='localhost', port=14711, parse_yaml=False)

colors = {
    'red' : Color(255, 0, 0),
    'green' : Color(0, 255, 0),
    'blue' : Color(0, 0, 255),
    'white' : Color(255, 255, 255),
}

# setup long-lived stateful LEDStrip instance
default_led_count = 32
led = LEDStrip(default_led_count)


def issue_all_off():
    led.fillOff()


# update:2:5:6:1.0:green:white:red:blue:red
# update:2:5:6:1.0:green:white_pulse:red:blue_pulse:red <<--ignore for now
def issue_update(tokens):
    led.setMasterBrightness(tokens[4])
    start_idx = tokens[1]
    segment_width = tokens[3]

    # green|blue|white|red)(_pulse)
    for i in range(tokens[2]):
        # Fill the strand (or a subset) with a single Color
        # def fill(self, color, start=0, end=0):
        led.fill('... colors[i + 5], start_idx, default_led_count ...')
        led.update()


# start_build:2:32:1.0
def issue_start_build(start_idx=0, led_count=32, brightness=1.0):
    led.setMasterBrightness(brightness)
    led.anim_larson_rainbow(2, 0.5)
    led.update()

    #larson scanner (i.e. Cylon Eye or K.I.T.T.) but Rainbow
    # def anim_larson_rainbow(self, tail=2, fade=0.75, start=0, end=0):


def issue_current_directive(directive):
    tokens = directive.split(':')
    if tokens[0] == 'all_off':
        issue_all_off()

    elif tokens[0] == 'start_build':
        issue_start_build(tokens[1], tokens[2], tokens[3])

    elif tokens[0] == 'update':
        issue_update(tokens)


def main():
    try:
        directive = 'all_off'
        job = None
        last_second = time.localtime().tm_sec
        while True:
            issue_current_directive(directive)

            now = time.localtime().tm_sec
            if now != last_second:
                last_second = now
                print 'polling..'
                job = beanstalk.reserve(timeout=0)
                if job is not None:
                    print "job found with content: {0}".format(job.body)
                    directive = job.body
                    job.delete()

            sleep(0.03) # loop fast enough for animations ---> this could be altered per directive if reqd

    except KeyboardInterrupt:
        print '^C received, shutting down controller'
        led.all_off()

if __name__ == '__main__':
    main()    