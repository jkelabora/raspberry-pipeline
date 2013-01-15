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
    if value_for('all_off', query): 
        return 'all_off'
    else:
        default_brightness = 1.0 # 0.0 -> 1.0
        default_led_count = 32
        default_segment_count = 5
        segment_count = value_for('segment_count', query) if value_for('segment_count', query) else default_segment_count
        led_start_offset = default_led_count % segment_count

        # start_build=true -> respect defaults, ignore other params
        if value_for('start_build', query):
            start_led_index = led_start_offset
            end_led_index = default_led_count
            return 'start_build:{0}:{1}:{2}'.format(start_led_index, end_led_index, default_brightness)
        
        # seg_(1 < n < segment_count)=(red,green,blue,white)[_pulse]
        # segment_width = default_led_count / segment_count
        return None

class LightSwitch(BaseHTTPRequestHandler):

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
                self.send(400, 'Bad request')
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
