$ brew install beanstalkd
$ beanstalkd -l 127.0.0.1 -p 14711

RPi-build-lights $ sudo python webserver.py 

RPi-build-lights $ python lights-controller.py 

http://localhost:666/index.html?key=value
