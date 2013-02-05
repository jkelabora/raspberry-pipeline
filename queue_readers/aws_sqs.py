##############

# read message api
#: queue_name => String
#: read_next => String(message body) or None
#: delete_last


# $ git clone https://github.com/boto/boto.git
# $ cd boto
# $ python setup.py install



import boto.sqs
# conn = boto.sqs.connect_to_region("us-east-1", aws_access_key_id='<aws access key'>, aws_secret_access_key='<aws secret key>')
conn = boto.sqs.connect_to_region('ap-southeast-2') #assumes AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY env var's

# Queue(https://queue.amazonaws.com/411358162645/myqueue)
q = conn.get_queue('raspberry-pipeline')

# return the message read or it will return None if no messages were available
m = q.read() # optional visibility timeout integer in seconds
m.get_body()


q.delete_message(m)
