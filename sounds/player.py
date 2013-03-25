import os
from random import randrange
import glob
import logging
import subprocess
import signal

log = logging.getLogger()

class Player:

    def play_random_start_sound(self):
        self.play_this_thing(self.randomly_choose_mp3_in_sub_directory("start_build"))

    def play_random_success_sound(self):
        self.play_this_thing(self.randomly_choose_mp3_in_sub_directory("success"))

    def play_random_failure_sound(self):
        self.play_this_thing(self.randomly_choose_mp3_in_sub_directory("failure"))

    def play_this_thing(self, filename):
        self.kill_off_any_currently_playing_sounds()
        log.info("playing {0}...".format(filename))
        os.system("mpg321 {0} &".format(filename))

    def kill_off_any_currently_playing_sounds(self):
        proc = subprocess.Popen(["pgrep", 'mpg321'], stdout=subprocess.PIPE)
        for pid in proc.stdout:
            log.info("killing off mpg321 process with PID {0}...".format(pid))
            os.kill(int(pid), signal.SIGTERM) # there are other variants if this doesn't do the trick

    def randomly_choose_mp3_in_sub_directory(self, sub_directory):
        directory = "{0}/sounds/{1}/".format(os.environ['RPI_HOME'], sub_directory)
        files = glob.glob("{0}*.mp3".format(directory))
        return files[randrange(len(files))]

