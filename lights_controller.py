# script expects RPI_HOME to be set as an env var

import time
import re
import os
from time import sleep
import Queue
from lib.LPD8806 import *
from queue_readers.aws_sqs import *
import os
import logging

logging.basicConfig(filename="{0}/logs/pipeline.log".format(os.environ['RPI_HOME']), level=logging.INFO, format="%(asctime)s <%(threadName)s>: %(message)s", datefmt='%m/%d/%Y %I:%M:%S %p')
log = logging.getLogger()

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


# update_segment:2:6:3:1.0:green
def issue_update_segment(tokens):
    led.setMasterBrightness(float(tokens[4]))
    start_idx = int(tokens[1])
    segment_width = int(tokens[2])
    seg_start_idx = (int(tokens[3]) - 1) * segment_width + start_idx
    seg_end_idx = seg_start_idx + segment_width - 1
    seg_color = colors[tokens[5]]
    # Fill the strand (or a subset) with a single Color
    # def fill(self, color, start=0, end=0):
    led.fill(seg_color, seg_start_idx, seg_end_idx)
    led.update()


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
        # Fill the strand (or a subset) with a single Color
        # def fill(self, color, start=0, end=0):
        led.fill(seg_color, seg_start_idx, seg_end_idx)
        led.update()


# start_build:2:0.5:0:0:1.0
def issue_start_build(tail=2, fade=0.5, start_idx=0, end_idx=0, brightness=1.0):
    led.setMasterBrightness(brightness)

    #larson scanner (i.e. Cylon Eye or K.I.T.T.) but Rainbow
    # def anim_larson_rainbow(self, tail=2, fade=0.75, start=0, end=0):
    led.anim_larson_rainbow(tail, fade, start_idx, end_idx)
    led.update()

#---------
jenkins_segments = {
    'Prepare' : 0,
    'Unit Tests' : 1,
    'Integration Tests' : 2,
    'Deploy Test' : 3,
    'Deploy to QA' : 4
}

jenkins_colors = {
    'FAILURE' : 'red',
    'SUCCESS' : 'green',
    'ABORTED' : 'white'
}

jenkins_regex = r"Build ([A-Z]+): (.*) #"

def jenkins_color(message):
    match = re.search(jenkins_regex, message)
    return jenkins_colors[match.group(1)]

def jenkins_segment(message):
    match = re.search(jenkins_regex, message)
    return jenkins_segments[match.group(2)]


def randomly_choose_mp3(directory):
    from random import randrange
    import glob
    files = glob.glob("{0}*.mp3".format(directory))
    return files[randrange(len(files))]

def play_this_thing(filename):
    log.info("playing {0}...".format(filename))
    os.system("mpg321 {0} &".format(filename))

def issue_current_jenkins_directive(directive, play_sound):

    if directive == 'all_off':
        issue_all_off()
        return

    color = jenkins_color(directive)
    segment_number = jenkins_segment(directive)
    if segment_number == 0:
        issue_start_build()
        if play_sound:
          play_this_thing(randomly_choose_mp3("{0}/sounds/start_build/".format(os.environ['RPI_HOME'])))
        return

    if play_sound:
      if color == 'green':
        play_this_thing(randomly_choose_mp3("{0}/sounds/success/".format(os.environ['RPI_HOME'])))
      elif color == 'red':
        play_this_thing(randomly_choose_mp3("{0}/sounds/failure/".format(os.environ['RPI_HOME'])))

    if segment_number == 1:
        issue_update(['update','2','5','6','1.0',color,'blue','blue','blue','blue'])

    # update_segment:2:6:3:1.0:green
    tokens = ['update_segment', '2', '6', segment_number, '1.0', color]
    issue_update_segment(tokens)
#---------


def issue_current_directive(directive):
    tokens = directive.split(':')
    if tokens[0] == 'all_off':
        issue_all_off()

    elif tokens[0] == 'start_build':
        issue_start_build(int(tokens[1]), float(tokens[2]), int(tokens[3]), int(tokens[4]), float(tokens[5]))

    elif tokens[0] == 'update':
        issue_update(tokens)

    elif tokens[0] == 'update_segment':
        issue_update_segment(tokens)


def main():

    local_q = Queue.Queue()
    PollSQSWorker(local_q).start() # start a thread to poll for messages on the sqs queue

    directive = 'all_off'
    play_sound = False

    while True:
        try:
            issue_current_jenkins_directive(directive, play_sound)
            play_sound = False

            job = local_q.get_nowait() # this will normally throw Queue.Empty

            log.info('proceeding to process message passed to local queue..')
            directive = job
            play_sound = True
            local_q.task_done()
            PollSQSWorker(local_q).start() # old thread has terminated so start another one to poll sqs queue

        except Queue.Empty:
            sleep(0.03) # loop fast enough for animations ---> this could be altered per directive if reqd

        except KeyboardInterrupt:
            log.info('^C received, shutting down controller')
            led.all_off()
            sys.exit()

if __name__ == '__main__':
    main()
