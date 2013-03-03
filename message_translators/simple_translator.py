# deals with messages that are closer to those in the base interface
# could be used when in full control of the message structure - like when using the provided sqs java example:

# cd aws-java-sdk-1.3.30/samples/AmazonSimpleQueueService
# echo "accessKey=[--INSERT--]" > AwsCredentials.properties && echo "secretKey=[--INSERT--]" >> AwsCredentials.properties
# ant -Darg0="ap-southeast-2" -Darg1="raspberry-pipeline" -Darg2="all_off" run

# examples messages:
# "start_build"
# "update_segment:2:6:3:1.0:green"
# "update:2:5:6:1.0:green:white:red:blue:red"
# "all_off"

from lib.base_message_interface import BaseMessageInterface

class SimpleMessageTranslator:

    def __init__(self):
        self.base_message_interface = BaseMessageInterface()

    def issue_current_directive(self, directive, play_sound=False):
        tokens = directive.split(':')

        if tokens[0] == 'all_off':
            self.base_message_interface.issue_all_off()

        elif tokens[0] == 'start_build':
            self.base_message_interface.issue_start_build()

        elif tokens[0] == 'update':
            self.base_message_interface.issue_update(tokens[1:])

        elif tokens[0] == 'update_segment':
            self.base_message_interface.issue_update_segment(tokens[1:])
