A lightweight webserver which communicates via a simple message queue with a Raspberry Pi LED-strip control script - designed as an easy to use build pipeline monitor.

```
$ git clone git://github.com/boto/boto.git
$ cd boto
$ sudo python setup.py install

sudo cp scripts/raspberry-pipeline /etc/init.d/
sudo update-rc.d raspberry-pipeline defaults

sudo /etc/init.d/raspberry-pipeline {start|stop}


cd aws-java-sdk-1.3.30/samples/AmazonSimpleQueueService
echo "accessKey=[--INSERT--]" > AwsCredentials.properties && echo "secretKey=[--INSERT--]" >> AwsCredentials.properties
ant -Darg0="ap-southeast-2" -Darg1="raspberry-pipeline" -Darg2="start_build:2:0.5:0:0:1.0" run

```
