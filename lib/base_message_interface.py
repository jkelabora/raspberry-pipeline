# provides a set of messages to drive a stateful instance of a led strip driver.
# animations (like issue_start_build) need to called repeatedly from a loop outside of this class.
# available messages:

# 1a) issue_start_first_build()
#  - run the default animation for signalling the start of the build for the first pipeline

# 1b) issue_start_second_build()
#  - run the default animation for signalling the start of a build for the secone pipeline

# 2) issue_update_segment(tokens)
#  - update a single segment of the stip to a given colour (out of the colours defined above)
#  - example tokens    ['2', '6', '3', '1.0', 'green']
#  - token description [start_led_0-based-index='2', segment_led_width='6', segment_number='3',
#                       master_brightness='1.0', segment_colour='green']

# 3) issue_update(tokens)
#  - update all the segments of a strip at once
#  - expects that there are segment_count segment colour tokens (each a valid colour as defined above)
#  - example tokens    ['2', '5', '6', '1.0', 'green', 'white', 'red', 'blue', 'red']
#  - token description [start_led_0-based-index='2', segment_count='5', segment_width='6', master_brightness='1.0',
#                       1st_segment_colour='green', 2nd_segment_colour='white', 3rd_segment_colour='red',
#                       4th_segment_colour='blue', 5th_segment_colour='red']

# 4) issue_all_off()
#  - does what you think

from lib.colour import Colour
from lib.ledstrip import Strand
import collections

colours = {
    'red' : Colour(255, 0, 0),
    'green' : Colour(0, 255, 0),
    'blue' : Colour(0, 0, 255),
    'white' : Colour(255, 255, 255)
}

base_animation_colours = [[0,0,250],[0,0,225],[0,0,200],[0,0,175],[0,0,150],[0,0,125],[0,0,100],[0,0,75],[0,0,50],[0,0,25],
    [0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],
    [0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]

class BaseMessageInterface:

    def __init__(self, default_led_count=32):
        self.led = Strand(default_led_count) # long-lived stateful LEDStrip instance

        self.first_led_range = collections.deque(xrange(len(base_animation_colours[0:20])))
        self.second_led_range = collections.deque(xrange(len(base_animation_colours[0:12])))

    def issue_start_first_build(self):
        for x in xrange(0, 19):
            self.first_led_range.rotate(1)
            self.led.set(x, base_animation_colours[self.first_led_range[0]][0],
                base_animation_colours[self.first_led_range[0]][1], base_animation_colours[self.first_led_range[0]][2])
        self.first_led_range.rotate((len(self.first_led_range)-1))

    def issue_start_second_build(self):
        for x in xrange(0, 11):
            self.second_led_range.rotate(1)
            self.led.set(x, base_animation_colours[self.second_led_range[0]][0],
                base_animation_colours[self.second_led_range[0]][1], base_animation_colours[self.second_led_range[0]][2])
        self.second_led_range.rotate((len(self.second_led_range)-1))

    def issue_update_segment(self, tokens):
        start_idx = int(tokens[0])
        segment_width = int(tokens[1])
        seg_start_idx = (int(tokens[2]) - 1) * segment_width + start_idx
        seg_end_idx = seg_start_idx + segment_width
        seg_colour = colours[tokens[3].lower()]
        self.led.fill(seg_colour.R, seg_colour.G, seg_colour.B, seg_start_idx, seg_end_idx)
        self.led.update()

    def issue_update(self, tokens):
        start_idx = int(tokens[0])
        segment_count = int(tokens[1])
        segment_width = int(tokens[2])

        for i in range(segment_count):
            seg_colour = colours[tokens[i + 3].lower()]
            seg_start_idx = i * segment_width + start_idx
            seg_end_idx = seg_start_idx + segment_width - 1
            self.led.fill(seg_colour.R, seg_colour.G, seg_colour.B, seg_start_idx, seg_end_idx)
            self.led.update()

    def issue_all_off(self):
        self.led.fill(0,0,0)
