A lightweight webserver which communicates via a simple message queue with a Raspberry Pi LED-strip control script - designed as an easy to use build pipeline monitor.

```
tar czf raspberry-pipeline.tar.gz raspberry-pipeline/
scp raspberry-pipeline.tar.gz pi@raspberrypi.local:/home/pi

tar -xvzf raspberry-pipeline.tar.gz 
wget https://github.com/downloads/kr/beanstalkd/beanstalkd-1.8.tar.gz
tar -xvzf beanstalkd-1.8.tar.gz
beanstalkd-1.8/
make

$ git clone git://github.com/boto/boto.git
$ cd boto
$ sudo python setup.py install

cd beanstalkd-1.8/
./beanstalkd -l 127.0.0.1 -p 14711 &
cd ../raspberry-pipeline/
sudo python beanstalk_webserver.py &
sudo python lights_controller.py &

(fg ^C to kill)


http://raspberrypi.local:3142/start_build.html
http://raspberrypi.local:3142/all_off.html

http://raspberrypi.local:3142/update.html?seg_1=green&seg_2=white&seg_3=red&seg_4=blue&seg_5=red
http://raspberrypi.local:3142/update.html?seg_1=green&seg_2=white&seg_3=red&seg_4=blue&seg_5=red&debug=true


to finish (one optional 'pulse' segment per command):
http://raspberrypi.local:3142/update.html?seg_1=green&seg_2=white_pulse&seg_3=red&seg_4=bluee&seg_5=red


cd aws-java-sdk-1.3.30/samples/AmazonSimpleQueueService
echo "accessKey=[--INSERT--]" > AwsCredentials.properties && echo "secretKey=[--INSERT--]" >> AwsCredentials.properties
ant -Darg0="ap-southeast-2" -Darg1="raspberry-pipeline" -Darg2="start_build:2:0.5:0:0:1.0" run

```
