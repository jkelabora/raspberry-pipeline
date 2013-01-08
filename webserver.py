from urlparse import urlparse
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import beanstalkc

def determine_message(query):
    message = query
    if query.find('debug') > 0:
        message += ' DEBUG'
    return message

class LightSwitch(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.find(".html") > 0:

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
        port = 666
        server = HTTPServer(('', port), LightSwitch)
        print 'started httpserver on port %d...' % port
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()
