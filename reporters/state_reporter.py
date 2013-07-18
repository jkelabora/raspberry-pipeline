# gather the state of all pipelines for publishing elsewhere

import threading
import logging
from time import sleep
import os

class StateReporter(threading.Thread):

  def __init__(self, reporter_q):
    threading.Thread.__init__(self) # required when extending threading.Thread
    self.daemon = True # so that this thread get killed when the main thread does

    self.reporter_q = reporter_q
    logging.getLogger().info('new pipeline(s) state reporter thread started..')

  def run(self):
    while True:
      sleep(5.0)
      logging.getLogger().info("getting pipeline(s) status...")

      try:
        report = reporter_q.get_nowait() # this will normally throw Queue.Empty
      except Queue.Empty:
        pass

      if report is not None:
        logging.getLogger().info("latest status is: {0}".format(report.get_body()))
        # push info to os.environ['SOME_PLACE']
        # rest api post ?

        # delete all messages
        while reporter_q.empty() is False:
          try:
            reporter_q.get_nowait()
          except Queue.Empty:
            pass
