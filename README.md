A lightweight webserver which communicates via a simple message queue with a Raspberry Pi LED-strip control script - designed as an easy to use build pipeline monitor.

```
$ brew install beanstalkd
$ beanstalkd -l 127.0.0.1 -p 14711

RPi-build-lights $ sudo python webserver.py 

RPi-build-lights $ python lights-controller.py 

http://localhost:666/index.html?key=value
```
