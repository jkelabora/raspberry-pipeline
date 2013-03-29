import collections
from lib.base_message_interface import BaseMessageInterface

base_animation_colours = [[0,0,250],[0,0,225],[0,0,200],[0,0,175],[0,0,150],[0,0,125],[0,0,100],[0,0,75],[0,0,50],[0,0,25],
    [0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],
    [0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]

# the underlying LEDStrip needs all updates issued to it across Pipline instances to come via
# this single shared instance of BaseMessageInterface
base_message_interface = BaseMessageInterface()

class Pipeline:

    def __init__(self, detail):
        self.detail = detail
        self.led_range = collections.deque(xrange(self.full_length()))

    def full_length(self):
        return self.detail['STAGE_WIDTH'] * (len(self.detail['STAGES']) -1) # excluding Prepare stage

    def issue_all_off(self):
        base_message_interface.issue_all_off()

    def issue_start_build(self):
        for pixel in xrange(self.detail['OFFSET'], self.detail['OFFSET'] + self.full_length()):
            self.led_range.rotate(1)
            base_message_interface.issue_start_build_step(pixel, base_animation_colours[self.led_range[0]][0],
                base_animation_colours[self.led_range[0]][1], base_animation_colours[self.led_range[0]][2])
        self.led_range.rotate((len(self.led_range)-1))

    def issue_all_stages_update(self, colour):
        tokens = [self.detail['OFFSET'], (len(self.detail['STAGES'])-1), self.detail['STAGE_WIDTH'], colour] # exclude the Prepare stage
        extras = ['blue'] * (len(self.detail['STAGES'])-2) # exclude the Prepare and first stages
        base_message_interface.issue_update(tokens + extras)

    def issue_update_segment(self, segment_number, colour):
        tokens = [self.detail['OFFSET'], self.detail['STAGE_WIDTH'], segment_number, colour]
        base_message_interface.issue_update_segment(tokens)
