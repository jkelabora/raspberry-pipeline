#!/usr/bin/python

from time import sleep
from LPD8806 import *

num = 32;
led = LEDStrip(num)
#led.setChannelOrder(ChannelOrder.BRG) #Only use this if your strip does not use the GRB order
#led.setMasterBrightness(0.5) #use this to set the overall max brightness of the strip
led.all_off()

#setup colors to loop through for fade
colors = [
	(255.0,0.0,0.0),
	(0.0,255.0,0.0),
	(0.0,0.0,255.0),
	(255.0,255.0,255.0),
]

step = 0.01
for c in range(4):
	r, g, b = colors[c]
	level = 0.01
	dir = step
	while level >= 0.0:
		led.fill(Color(r, g, b, level))
		led.update()
		if(level >= 0.99):
			dir = -step
		level += dir
		sleep(0.005)
		
led.all_off()

#animations - each animation method moves the animation forward one step on each call
#after each step, call update() to push it to the LED strip
#sin wave animations
color = Color(255, 0, 0)
for i in range(led.lastIndex):
	led.anim_wave(color, 4)
	led.update()
	sleep(0.15)
	
color = Color(0, 0, 100)
for i in range(led.lastIndex):
	led.anim_wave(color, 2)
	led.update()
	sleep(0.15)


#rolling rainbow
for i in range(384):
	led.anim_rainbow()
	led.update()
	
led.fillOff()
	
#evenly distributed rainbow
for i in range(384*2):
	led.anim_rainbow_cycle()
	led.update()
	
led.fillOff()

#setup colors for wipe and chase
colors = [
	Color(255, 0, 0),
	Color(0, 255, 0),
	Color(0, 0, 255),
	Color(255, 255, 255),
]

for c in range(4):
	for i in range(num):
		led.anim_color_wipe(colors[c])
		led.update()
		sleep(0.03)
	
led.fillOff()
	
for c in range(4):
	for i in range(num):
		led.anim_color_chase(colors[c])
		led.update()
		sleep(0.03)
		
led.fillOff()

#scanner: single color and changing color
color = Color(255, 0, 0)
for i in range(led.lastIndex*4):
	led.anim_larson_scanner(color)
	led.update()
	sleep(0.03)

led.fillOff()

for i in range(led.lastIndex*4):
	led.anim_larson_rainbow(2, 0.5)
	led.update()
	sleep(0.03)

led.all_off()



