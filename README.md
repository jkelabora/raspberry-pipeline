A lightweight webserver which communicates via a simple message queue with a Raspberry Pi LED-strip control script - designed as an easy to use build pipeline monitor.

```
tar zxvf beanstalkd-1.8.tar.gz
cd beanstalkd-1.8/
make

beanstalkd -l 127.0.0.1 -p 14711 &
sudo python webserver.py &
python lights-controller.py &
(fg ^C to kill)

http://localhost:3142/start_build.html

http://localhost:3142/update.html?seg_1=green&seg_2=white_pulse&seg_3=red&seg_4=blue_pulse&seg_5=red
http://localhost:3142/update.html?seg_1=green&seg_2=white_pulse&seg_3=red&seg_4=blue_pulse&seg_5=red&debug=true

http://localhost:3142/all_off.html
```
