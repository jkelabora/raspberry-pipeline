import collections
from lib.base_message_interface import BaseMessageInterface
import re

# determined using http://hexcolortool.com/
base_animation_colours = [[255,127,255],[255,102,255],[255,77,255],[238,51,255],[213,26,255],[187,0,250],[162,0,225],[136,0,199],[111,0,174],[85,0,148],
  [60,0,123],[35,0,98],[9,0,72],[0,0,47],[0,0,21],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],
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
        return re.match('^' + self.detail['IDENTIFIER'], build_name)

    def current_state(self):
        return { self.detail['IDENTIFIER'] : self.state }

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

