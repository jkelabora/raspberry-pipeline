import beanstalkc
from time import sleep

beanstalk = beanstalkc.Connection(host='localhost', port=14711, parse_yaml=False)

def main():
    try:
        while True:
            print 'polling..'
            job = beanstalk.reserve(timeout=0)
            if job is not None:
                print "job found with content: %s" % job.body
                job.delete()
            sleep(0.50)

    except KeyboardInterrupt:
        print '^C received, shutting down controller'

if __name__ == '__main__':
    main()    