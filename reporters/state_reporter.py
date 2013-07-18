# gather the state of all pipelines for publishing elsewhere

import threading
import logging
from time import sleep
import os

class StateReporter(threading.Thread):

  def __init__(self, translator):
    threading.Thread.__init__(self) # required when extending threading.Thread
    self.daemon = True # so that this thread get killed when the main thread does

    self.translator = translator
    logging.getLogger().info('new pipeline(s) state reporter thread started..')

  def run(self):
    while True:
      sleep(2.0)
      logging.getLogger().info("full state is '{0}'..".format(translator.current_state()))

      # push info to os.environ['SOME_PLACE']
      # rest api post ?