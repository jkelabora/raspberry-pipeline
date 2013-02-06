import time
from time import sleep
import re
from LPD8806 import *

import boto.sqs
# conn = boto.sqs.connect_to_region("ap-southeast-2", aws_access_key_id='aws access key', aws_secret_access_key='aws secret key')
conn = boto.sqs.connect_to_region('ap-southeast-2') #assumes AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY env var's
q = conn.get_queue('raspberry-pipeline')

#import os
#print os.environ['AWS_ACCESS_KEY_ID']
#print os.environ['AWS_SECRET_ACCESS_KEY']

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
    led.all_off()


# update:2:5:6:1.0:green:white:red:blue:red
# update:2:5:6:1.0:green:white_pulse:red:blue_pulse:red <<--ignore _pulse elements for now
def issue_update(tokens):
    led.setMasterBrightness(float(tokens[4]))
    start_idx = int(tokens[1])
    segment_count = int(tokens[2])
    segment_width = int(tokens[3])

    for i in range(segment_count):
        seg_color = colors[tokens[i + 5]]
        seg_start_idx = i * segment_width + start_idx
        seg_end_idx = seg_start_idx + segment_width - 1
        print "for segment {0}, sending seg_color:{1}, seg_start_idx:{2}, seg_end_idx:{3}".format(i + 1, tokens[i + 5], seg_start_idx, seg_end_idx)
        # Fill the strand (or a subset) with a single Color
        # def fill(self, color, start=0, end=0):
        led.fill(seg_color, seg_start_idx, seg_end_idx)
        led.update()


# start_build:2:32:1.0
def issue_start_build(start_idx=0, led_count=32, brightness=1.0):
    led.setMasterBrightness(brightness)

    #larson scanner (i.e. Cylon Eye or K.I.T.T.) but Rainbow
    # def anim_larson_rainbow(self, tail=2, fade=0.75, start=0, end=0):
    led.anim_larson_rainbow(2, 0.5)
    led.update()


def issue_current_directive(directive):
    tokens = directive.split(':')
    if tokens[0] == 'all_off':
        issue_all_off()

    elif tokens[0] == 'start_build':
        issue_start_build(tokens[1], tokens[2], float(tokens[3]))

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
                job = q.read()
                if job is not None:
                    print "job found with content: {0}".format(job.get_body())
                    directive = job.get_body()
                    q.delete_message(job)

            sleep(0.03) # loop fast enough for animations ---> this could be altered per directive if reqd

    except KeyboardInterrupt:
        print '^C received, shutting down controller'
        led.all_off()

if __name__ == '__main__':
    main()    