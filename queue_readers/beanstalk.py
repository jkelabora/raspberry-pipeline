##############

# read message api
#: queue_name => String
#: read_next => String(message body) or None
#: delete_last

import beanstalkc
beanstalk = beanstalkc.Connection(host='localhost', port=14711, parse_yaml=False)

print 'polling..'
job = beanstalk.reserve(timeout=0)
if job is not None:
    print "job found with content: {0}".format(job.body)
    directive = job.body
    job.delete()
