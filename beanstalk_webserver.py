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


default_brightness = 1.0 # 0.0 -> 1.0
default_led_count = 32
default_segment_count = 5

def segment_count(query):
    return value_for('segment_count', query) if value_for('segment_count', query) else default_segment_count

def led_start_offset(query):
    return default_led_count % segment_count(query)

def create_start_build_message(query):
    return 'start_build:{0}:{1}:{2}'.format(led_start_offset(query), default_led_count, default_brightness)

def create_update_message(query):
    # http://raspberrypi:3142/update.html?update=true&seg_1=green&seg_2=white_pulse&seg_3=red&seg_4=blue_pulse&seg_5=white&debug=true
    # return a message with segment directives ordered by segment index if possible
    segment_width = default_led_count / segment_count(query)
    message = "update:{0}:{1}:{2}:{3}".format(led_start_offset(query), segment_count(query), segment_width, default_brightness)
    for i in range(segment_count(query)):
        led_idx = i + 1
        led_directive = value_for('seg_{0}'.format(led_idx), query)
        if led_directive == None:
            print "with {0} segments, expected a 'seg_{1}=' key".format(segment_count(query), led_idx)
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

def handle_message(message, resp, debug_mode=False):
    output = ''
    if debug_mode:
        output = "DEBUG: message posted: 'content' => '{0}'".format(message)
    else:
        beanstalk = beanstalkc.Connection(host='localhost', port=14711, parse_yaml=False)
        msg_id = beanstalk.put(message)
        output = "INFO: message posted: 'id':'content' => '{0}':'{1}'".format(msg_id, message)
    print output
    resp.send_response(200)
    resp.send_header('Content-type', 'text/html')
    resp.end_headers()
    resp.wfile.write("<html><b>All good.. Posted message: '{0}'</b></html>".format(output))

class LightSwitch(BaseHTTPRequestHandler):
    def do_GET(self):
        url = self.path
        parsed_query = urlparse(url).query.lower()
        debug_mode = re.search('debug', parsed_query)
        if re.search('all_off.html', url):
            handle_message('all_off', self, debug_mode)

        elif re.search('start_build.html', url):
            handle_message(create_start_build_message(parsed_query), self, debug_mode)

        elif re.search('update.html', url):
            message = create_update_message(parsed_query)
            if message: 
                handle_message(message, self, debug_mode)
            else:
                self.send_error(400, 'Bad request')
        else:
            self.send_error(404, 'Path not found')
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
