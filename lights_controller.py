# script expects RPI_HOME to be set as an env var

import time
import re
import os
from time import sleep
import Queue
from queue_readers.aws_sqs import *
from lib.base_message_interface import *
import os
import logging

logging.basicConfig(level=logging.INFO,
    filename="{0}/logs/pipeline.log".format(os.environ['RPI_HOME']),
    format="%(asctime)s <%(threadName)s>: %(message)s", datefmt='%m/%d/%Y %I:%M:%S %p')
log = logging.getLogger()

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


message_interface = BaseMessageInterface()


def issue_current_jenkins_directive(directive, play_sound):

    if directive == 'all_off':
        message_interface.issue_all_off()
        return

    color = jenkins_color(directive)
    segment_number = jenkins_segment(directive)
    if segment_number == 0:
        message_interface.issue_start_build()
        if play_sound:
          play_this_thing(randomly_choose_mp3("{0}/sounds/start_build/".format(os.environ['RPI_HOME'])))
        return

    if play_sound:
      if color == 'green':
        play_this_thing(randomly_choose_mp3("{0}/sounds/success/".format(os.environ['RPI_HOME'])))
      elif color == 'red':
        play_this_thing(randomly_choose_mp3("{0}/sounds/failure/".format(os.environ['RPI_HOME'])))

    if segment_number == 1:
        message_interface.issue_update(['2','5','6','1.0',color,'blue','blue','blue','blue'])

    tokens = ['2', '6', segment_number, '1.0', color]
    message_interface.issue_update_segment(tokens)
#---------


def issue_current_directive(directive):
    tokens = directive.split(':')
    if tokens[0] == 'all_off':
        issue_all_off()

    elif tokens[0] == 'start_build':
        issue_start_build()

    # update:2:5:6:1.0:green:white:red:blue:red
    elif tokens[0] == 'update':
        issue_update(tokens[1:])

    # update_segment:2:6:3:1.0:green
    elif tokens[0] == 'update_segment':
        issue_update_segment(tokens[1:])


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
