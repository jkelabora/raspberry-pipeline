from urlparse import urlparse
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import beanstalkc
import re

def value_for(key, source):
    regex = r"\b(" + re.escape(key) + r")=(\w+)\b"
    match = re.search(regex, source)
    return match.group(2) if match else None

def determine_message(query):

    default_led_count = 32
    default_brightness = 1.0 # 0.0 -> 1.0
    default_segment_count = 5

    segment_count = value_for('segment_count', query) if value_for('segment_count', query) else default_segment_count

    # all_off=true     -> ignore all other params
    # start_build=true -> ignore all other params


    # seg_(1 < n < segment_count)=(red,green,blue,white)[_pulse]


    message = query

    return message

class LightSwitch(BaseHTTPRequestHandler):

    def do_GET(self):
        if re.search('.html', self.path):

            parsed = urlparse(self.path).query
            message = determine_message(parsed)

            if re.search('debug', parsed) == False:
                beanstalk = beanstalkc.Connection(host='localhost', port=14711, parse_yaml=False)
                msg_id = beanstalk.put(message)
                print "INFO: message posted: 'id':'content' => '{0}':'{1}'".format(msg_id, message)
            else:
                print "DEBUG: message posted: 'content' => '{0}'".format(message)

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write("<html><b>All good..</b></html>");
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
