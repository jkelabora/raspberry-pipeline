from lib.LPD8806 import Color
from lib.LPD8806 import LEDStrip

colours = {
    'red' : Color(255, 0, 0),
    'green' : Color(0, 255, 0),
    'blue' : Color(0, 0, 255),
    'white' : Color(255, 255, 255),
}

# provides a set of messages to drive a stateful instance of a led strip driver.
# animations (like issue_start_build) need to called repeatedly from a loop outside of this class.
# available messages:

# 1) issue_start_build()
#  - run the default animation for signalling the start of a build
#  - default arguments provided (can be overridden if need be)

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

class BaseMessageInterface:

    def __init__(self, default_led_count=32):
        self.led = LEDStrip(default_led_count) # long-lived stateful LEDStrip instance

    def issue_start_build(self, tail=2, fade=0.5, start_idx=0, end_idx=0, brightness=1.0):
        self.led.setMasterBrightness(brightness)

        self.led.anim_larson_rainbow(tail, fade, start_idx, end_idx)
        self.led.update()

    def issue_update_segment(self, tokens):
        self.led.setMasterBrightness(float(tokens[3]))

        start_idx = int(tokens[0])
        segment_width = int(tokens[1])
        seg_start_idx = (int(tokens[2]) - 1) * segment_width + start_idx
        seg_end_idx = seg_start_idx + segment_width - 1
        seg_color = colours[tokens[4].lower()]
        self.led.fill(seg_color, seg_start_idx, seg_end_idx)
        self.led.update()

    def issue_update(self, tokens):
        self.led.setMasterBrightness(float(tokens[3]))

        start_idx = int(tokens[0])
        segment_count = int(tokens[1])
        segment_width = int(tokens[2])

        for i in range(segment_count):
            seg_color = colours[tokens[i + 4]]
            seg_start_idx = i * segment_width + start_idx
            seg_end_idx = seg_start_idx + segment_width - 1
            self.led.fill(seg_color, seg_start_idx, seg_end_idx)
            self.led.update()

    def issue_all_off(self):
        self.led.all_off()
