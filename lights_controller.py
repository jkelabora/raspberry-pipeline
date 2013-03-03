# script expects RPI_HOME to be set as an env var

import os
import Queue
from time import sleep
import logging

from queue_readers.aws_sqs import PollSQSWorker
from message_translators.jenkins_translator import JenkinsMessageTranslator

logging.basicConfig(level=logging.INFO,
    filename="{0}/logs/pipeline.log".format(os.environ['RPI_HOME']),
    format="%(asctime)s <%(threadName)s>: %(message)s", datefmt='%m/%d/%Y %I:%M:%S %p')
log = logging.getLogger()

def main():

    translator = JenkinsMessageTranslator() # switch this out with something else if need be

    local_q = Queue.Queue()
    PollSQSWorker(local_q).start() # start a thread to poll for messages on the sqs queue

    directive = 'all_off'
    play_sound = False

    while True:
        try:
            translator.issue_current_directive(directive, play_sound)
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
