from __future__ import division
import time
import argparse
import math
import signal
import random
import sys
from Queue import Queue

from threading import Thread

from flask import Flask

import numpy as np
from scipy.interpolate import interp1d

from neopixel import *

app = Flask(__name__)



# LED strip configuration:
LED_COUNT      = 150      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering



# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=25):
	"""Wipe color across display a pixel at a time."""
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
		strip.show()
		time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
	"""Movie theater light style chaser animation."""
	for j in range(iterations):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, color)
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)

def rainbow(strip, wait_ms=20, iterations=1):
	"""Draw rainbow that fades across all pixels at once."""
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel((i+j) & 255))
		strip.show()
		time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
	"""Draw rainbow that uniformly distributes itself across all pixels."""
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
		strip.show()
		time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
	"""Rainbow movie theater light style chaser animation."""
	for j in range(256):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, wheel((i+j) % 255))
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)
def map_all(strip,func):
	for x,row in enumerate(led_map):
		for y,l in enumerate(row):
			c = led_colors[x][y]
			new_c = func(c) 
			if new_c != c:
				strip.setPixelColor(l,color_maxed(new_c))
				led_colors[x][y] = new_c

def map_leds(strip,color,wait_ms=5):
	diameter = 0
	centre = (
			random.randint(0,len(led_map[0])),
			random.choice([0,15,37])
		)
	while True:
		still_setting = False
		# Fade
		map_all(strip,lambda c: tuple([max(x-20,0) for x in c]))
		for x,row in enumerate(led_map):
			for y,l in enumerate(row):
				x_pos = x * len(row)/len(led_map)
				rel_x, rel_y = x_pos-centre[0], y-centre[1]
				dist = math.sqrt(rel_x**2 + rel_y**2) 
				if dist < diameter and diameter-1 < dist:
					color_brightened = random_brightness(color)
					strip.setPixelColor(l,color_maxed(color_brightened))
					led_colors[x][y] = color_brightened
					still_setting = True
		strip.show()
		#time.sleep(wait_ms/1000.0)
		if not still_setting and diameter > 5:
			break
		diameter += 0.5
	
def interpolate(colors, row, offset=0):
	spaces = np.linspace(0,len(row)*2,len(colors)*2-1)
	all_colors = colors+colors[:-1][::-1]
	interp = interp1d(spaces,all_colors,axis=0)
	return [(color_maxed(interp((i+offset) % (2*len(row)))),l) for i,l in enumerate(row)]
	

def meteors(strip,wait_ms=5):
	map_all(strip,lambda c: tuple([max(x-15,0) for x in c]))
	cooldown -= 1
	if random.random() < 0.05 and cooldown <= 0:
		cooldown = 20
		direction = random.choice([-1,1])
		shelves = [[led_map_and_index[0],led_map_and_index[1]],[led_map_and_index[2],led_map_and_index[3]]]
		shelf = random.choice(shelves)
		add_meteor(shelf[0][::direction],wheel_c(random.randint(0,255)))
		add_meteor(shelf[1][::direction],wheel_c(random.randint(0,255)))
	for color,leds in meteors:
		if not leds:
			meteors.remove((color,leds))
			continue
		led = leds.pop()
		l,(x,y) = led
		# set color
		add_color(x,y,random_brightness(color))
	strip.show()
	time.sleep(wait_ms/1000.0)
	

def rainbowy(strip, wait_ms=50):

	offset = 0
	while True:
		offset += 1	
		for c,l in interpolate([purple, white, purple], led_map[0],offset):
			strip.setPixelColor(l,c)
		for c,l in interpolate([orange, red], led_map[1],offset):
			strip.setPixelColor(l,c)
		for c,l in interpolate([green, blue], led_map[2],offset):
			strip.setPixelColor(l,c)
		for c,l in interpolate([red, orange], led_map[3],offset):
			strip.setPixelColor(l,c)
		strip.show()
	time.sleep(wait_ms/1000.0)


@app.route('/', methods=['GET','POST'])
def change_led():
	print("Hello")
	return "hi"

STOP = "stop"

def main_loop(strip, message_queue):
	while True:
		if not message_queue.empty():
			msg = message_queue.get()
			if msg == STOP:
				break
		print ('Color wipe animations.')
		#	colorWipe(strip, Color(255, 0, 0))  # Red wipe
		#	colorWipe(strip, Color(0, 255, 0))  # Blue wipe
		#	colorWipe(strip, Color(0, 0, 255))  # Green wipe
		#	print ('Theater chase animations.')
		#	theaterChase(strip, Color(127, 127, 127))  # White theater chase
		#	theaterChase(strip, Color(127,   0,   0))  # Red theater chase
		#	theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
		#	print ('Rainbow animations.')
		#	rainbow(strip)
		#	map_leds(strip, (255, 0, 0))  # Red wipe
		#	map_leds(strip, (0, 255, 0))  # Blue wipe
		#	map_leds(strip, (0, 0, 255))  # Green wipe
		meteors(strip)
		#	rainbowCycle(strip)
		#rainbowy(strip)
message_queue = Queue()
def startup():
	print("init")
	def signal_handler(signal, frame):
		print("stop")
		message_queue.put(STOP)
		colorWipe(strip, Color(0,0,0), wait_ms=1)
		sys.exit(0)
	signal.signal(signal.SIGINT, signal_handler)
	signal.signal(signal.SIGTERM, signal_handler)

	# Create NeoPixel object with appropriate configuration.
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
	# Intialize the library (must be called once before other functions).
	strip.begin()
	thread = Thread(target=main_loop,args=(strip,message_queue))
	thread.start()

startup()
