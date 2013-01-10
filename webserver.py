from urlparse import urlparse
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import beanstalkc
import re

def determine_message(query):

    default_led_count = 32
    default_brightness = 1.0 # 0.0 -> 1.0
    debug_mode = True if re.search('debug', query) else False

    message = query

    message = message + 'DEBUG' if debug_mode else message
    return message

class LightSwitch(BaseHTTPRequestHandler):

    def do_GET(self):
        if  re.search('.html', self.path):

            parsed = urlparse(self.path)
            print parsed

            beanstalk = beanstalkc.Connection(host='localhost', port=14711, parse_yaml=False)
            msg_id = beanstalk.put(determine_message(parsed.query))
            print "message posted with id: %d" % msg_id

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
        print 'started httpserver on port %d...' % port
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()
