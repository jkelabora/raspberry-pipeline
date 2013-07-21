import collections
from lib.base_message_interface import BaseMessageInterface
import re

base_animation_colours = [[250,125,0],[225,112,0],[200,100,0],[175,87,0],[150,75,0],[125,65,0],[100,50,0],[75,37,0],[50,25,0],[25,12,0],
    [0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],
    [0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]

# the underlying LEDStrip needs all updates issued to it across Pipline instances to come via
# this single shared instance of BaseMessageInterface
base_message_interface = BaseMessageInterface()

class Pipeline:

    def __init__(self, detail):
        self.detail = detail
        self.led_range = collections.deque(xrange(self.__full_length()))
        self.state = ['off'] * (len(self.detail['STAGES']) -1) # excluding Prepare stage

    def matches(self, build_name):
        return re.match('^' + self.detail['IDENTIFIER'], build_name):

    def current_state(self):
        return self.state

    def issue_all_off(self):
        meta = [self.detail['OFFSET'], (len(self.detail['STAGES'])-1), self.detail['STAGE_WIDTH']] # exclude the Prepare stage
        tokens = ['off'] * (len(self.detail['STAGES'])-1) # exclude the Prepare stage
        base_message_interface.issue_update(meta + tokens)
        self.state = tokens

    def issue_start_build(self):
        for pixel in xrange(self.detail['OFFSET'], self.detail['OFFSET'] + self.__full_length()):
            self.led_range.rotate(1)
            base_message_interface.issue_start_build_step(pixel, base_animation_colours[self.led_range[0]][0],
                base_animation_colours[self.led_range[0]][1], base_animation_colours[self.led_range[0]][2])
        self.led_range.rotate((len(self.led_range)-1))
        self.state = ['start'] * (len(self.detail['STAGES']) -1) # excluding Prepare stage

    def issue_all_stages_update(self, colour):
        tokens = [self.detail['OFFSET'], (len(self.detail['STAGES'])-1), self.detail['STAGE_WIDTH'], colour] # exclude the Prepare stage
        extras = ['blue'] * (len(self.detail['STAGES'])-2) # exclude the Prepare and first stages
        base_message_interface.issue_update(tokens + extras)
        self.state = [colour] + extras

    def issue_update_segment(self, segment_number, colour):
        tokens = [self.detail['OFFSET'], self.detail['STAGE_WIDTH'], segment_number, colour]
        base_message_interface.issue_update_segment(tokens)
        self.state[segment_number -1] = colour

    def __full_length(self):
        return self.detail['STAGE_WIDTH'] * (len(self.detail['STAGES']) -1) # excluding Prepare stage

