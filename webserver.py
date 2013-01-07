from urlparse import urlparse
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import beanstalkc

class LightController(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.find(".html") > 0:

            parsed = urlparse(self.path)
            print parsed

            beanstalk = beanstalkc.Connection(host='localhost', port=14711, parse_yaml=False)
            msg_id = beanstalk.put(parsed.query)
            print "message posted with id: %d" % msg_id

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write("<html><b>200 OK</b></html>");
            return
        else:
            self.send_error(404, 'Path not found')
            return
        return
                
def main():
    try:
        port = 666
        server = HTTPServer(('', port), LightController)
        print 'started httpserver on port %d...' % port
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()
