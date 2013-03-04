Raspberry Pi (Type B)

Occidentalis v0.2

http://learn.adafruit.com/adafruit-raspberry-pi-educational-linux-distro/overview


http://learn.adafruit.com/light-painting-with-raspberry-pi/hardware

* https://www.adafruit.com/products/306 (Digital RGB LED Weatherproof Strip 32 LED - (1m))

* http://www.adafruit.com/products/914 (Adafruit Pi Cobbler Breakout Kit for Raspberry Pi)

* https://www.adafruit.com/products/276 (5V 2A (2000mA) switching power supply - UL Listed)

* https://www.adafruit.com/products/368 (Female DC Power adapter - 2.1mm jack to screw terminal block)

* http://www.adafruit.com/products/578 (4-pin JST SM Plug + Receptacle Cable Set)


https://github.com/jkelabora/snsnotify-plugin

https://github.com/jkelabora/simple-message-generator.git

```
$ git clone git://github.com/boto/boto.git
$ cd boto
$ sudo python setup.py install

$ sudo apt-get install alsa-utils
$ sudo apt-get install mpg321

sudo cp scripts/raspberry-pipeline /etc/init.d/
sudo vi /etc/init.d/raspberry-pipeline         <-- will expect AWS creds by default.. update or remove as required
sudo update-rc.d raspberry-pipeline defaults

sudo /etc/init.d/raspberry-pipeline {start|stop}

```
