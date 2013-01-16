from urlparse import urlparse
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import beanstalkc
import re

def value_for(key, source):
    regex = r"\b(" + re.escape(key) + r")=(\w+)\b"
    match = re.search(regex, source)
    return match.group(2) if match else None

    # possible re-factor:
    # from urlparse import urlparse, parse_qsl
    # url = 'http://somesite.com/?foo=bar&key=val'
    # print parse_qsl(urlparse(url)[4])
    # [('foo', 'bar'), ('key', 'val')] --> a list of tuples

def determine_message(query):
    # all_off=true -> ignore all other params   
    # ============
    if value_for('all_off', query): 
        return 'all_off'
    else:
        default_brightness = 1.0 # 0.0 -> 1.0
        default_led_count = 32
        default_segment_count = 5
        segment_count = value_for('segment_count', query) if value_for('segment_count', query) else default_segment_count
        led_start_offset = default_led_count % segment_count

        # ============
        # start_build=true -> respect defaults, ignore other params
        if value_for('start_build', query):
            start_led_index = led_start_offset
            end_led_index = default_led_count
            return 'start_build:{0}:{1}:{2}'.format(start_led_index, end_led_index, default_brightness)
        
        # ============
        # http://localhost:3142/index.html?update=true&seg_1=green&seg_2=white_pulse&seg_3=red&seg_4=blue_pulse&seg_5=white
        if value_for('update', query):

            # return a message with segment directives ordered by segment index if possible
            segment_width = default_led_count / segment_count
            start_led_index = led_start_offset
            message = "update:{0}:{1}:{2}:{3}".format(start_led_index, segment_count, segment_width, default_brightness)
            for i in range(segment_count):
                led_idx = i + 1
                led_directive = value_for('seg_{0}'.format(led_idx), query)
                if led_directive == None:
                    print "with {0} segments, expected a 'seg_{1}=' key".format(segment_count, led_idx)
                    return None
                else:
                    colour = re.search(r"\b(green|blue|white|red)(_pulse)?\b", led_directive)
                    if colour:
                        print 'setting seg_{0} to {1}'.format(led_idx, colour.group())
                        message += ":{0}".format(colour.group())
                    else:
                        print "valid colour values are green|blue|white|red followed by an optional '_pulse' suffix, found {0} for seg_{1}".format(led_directive, led_idx)
                        return None
            return message
        return None

class LightSwitch(BaseHTTPRequestHandler):

    # todo: split this out into more entry points
    def do_GET(self):
        if re.search('.html', self.path):

            parsed = urlparse(self.path).query.lower()
            message = determine_message(parsed)

            if re.search('debug', parsed):
                print "DEBUG: message posted: 'content' => '{0}'".format(message)
            elif(message):
                beanstalk = beanstalkc.Connection(host='localhost', port=14711, parse_yaml=False)
                msg_id = beanstalk.put(message)
                print "INFO: message posted: 'id':'content' => '{0}':'{1}'".format(msg_id, message)
            else:
                self.send_error(400, 'Bad request')
                return

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write("<html><b>All good..</b></html>")
            return
        else:
            self.send_error(404, 'Path not found')
            return
        return

def main():
    try:
        port = 3142
        server = HTTPServer(('', port), LightSwitch)
        print 'started httpserver on port {0}...'.format(port)
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()
