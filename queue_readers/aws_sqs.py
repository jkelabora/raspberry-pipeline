# poll for messages on sqs (which can take a while), re-post found messages to local queue
# for main thread to process without latency

import boto.sqs
from boto.sqs.message import RawMessage
import threading
import logging
from time import sleep
import os

class PollSQSWorker(threading.Thread):

  def __init__(self, local_q):
    threading.Thread.__init__(self) # required when extending threading.Thread
    self.daemon = True # so that this thread get killed when the main thread does
    self.local_q = local_q

    conn = boto.sqs.connect_to_region(os.environ['SQS_REGION']) # assumes AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY env var's
    self.sqs_q = conn.get_queue(os.environ['SQS_QUEUE_NAME'])
    self.sqs_q.set_message_class(RawMessage)

    logging.getLogger().info('new SQS reader thread started..')

  def run(self):
    poll = True
    while poll:
      sleep(1.0)
      logging.getLogger().info("polling queue '{0}/{1}'..".format(os.environ['SQS_REGION'], os.environ['SQS_QUEUE_NAME']))
      job = self.sqs_q.read()
      if job is not None:
        logging.getLogger().info("job found with content: {0}".format(job.get_body()))
        self.local_q.put(job.get_body())
        self.sqs_q.delete_message(job)
        poll = False
