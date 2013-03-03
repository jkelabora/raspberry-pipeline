import os
from random import randrange
import glob
import logging

log = logging.getLogger()

class Player:

    def play_random_start_sound(self):
        self.play_this_thing(self.randomly_choose_mp3_in_sub_directory("start_build"))

    def play_random_success_sound(self):
        self.play_this_thing(self.randomly_choose_mp3_in_sub_directory("success"))

    def play_random_failure_sound(self):
        self.play_this_thing(self.randomly_choose_mp3_in_sub_directory("failure"))

    def play_this_thing(self, filename):
        log.info("playing {0}...".format(filename))
        os.system("mpg321 {0} &".format(filename))

    def randomly_choose_mp3_in_sub_directory(self, sub_directory):
        directory = "{0}/sounds/{1}/".format(os.environ['RPI_HOME'], sub_directory)
        files = glob.glob("{0}*.mp3".format(directory))
        return files[randrange(len(files))]

