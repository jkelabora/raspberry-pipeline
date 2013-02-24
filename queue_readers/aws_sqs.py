##############
# read message api
#: put last read message on local queue => String(message body) or None
##############

# $ git clone https://github.com/boto/boto.git
# $ cd boto
# $ python setup.py install

import boto.sqs
import sys
import threading
import logging

class SQS(threading.Thread):
  def __init__(self, local_q):
    threading.Thread.__init__(self)
    self.daemon = True
    self.local_q = local_q

    conn = boto.sqs.connect_to_region('ap-southeast-2') #assumes AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY env var's
    self.sqs_q = conn.get_queue('raspberry-pipeline')
    self.sqs_q.set_message_class(RawMessage)

    logging.getLogger().info('new SQS reader thread started..')

  def run(self):
    job = self.sqs_q.read(visibility_timeout=None, wait_time_seconds=sys.maxsize)
    logging.getLogger().info("job found with content: {0}".format(job.get_body()))
    self.local_q.put(job.get_body())
    self.sqs_q.delete_message(job)

