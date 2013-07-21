# gather the state of all pipelines for publishing elsewhere

import threading
import logging
from time import sleep
import os
import urllib2
import json

class StateReporter(threading.Thread):

  def __init__(self, reporter_q):
    threading.Thread.__init__(self) # required when extending threading.Thread
    self.daemon = True # so that this thread get killed when the main thread does

    self.reporter_q = reporter_q
    logging.getLogger().info('new pipeline(s) state reporter thread started..')

  def run(self):
    while True:
      sleep(10.0)
      logging.getLogger().info("getting pipeline(s) status...")

      try:
        report = self.reporter_q.get_nowait() # this will normally throw Queue.Empty
      except Queue.Empty:
        pass

      if report is not None:
        logging.getLogger().info("posting to {0} this status: {1} ".format(os.environ['REPORTING_ENDPOINT'], report))

        req = urllib2.Request(os.environ['REPORTING_ENDPOINT'])
        req.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(req, json.dumps(report))

        # delete all messages
        while self.reporter_q.empty() is False:
          try:
            self.reporter_q.get_nowait()
          except Queue.Empty:
            pass
