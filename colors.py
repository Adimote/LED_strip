#!/usr/bin/env python3
import time
import argparse
import math
import signal
import random
import sys
from queue import Queue

from threading import Thread

from flask import Flask, render_template, request



from state import State
from meteors import Meteors
from rainbowy import Rainbowy
from standards import colorWipe

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

message_queue = Queue()

@app.route('/', methods=['GET','POST'])
def change_led():
	if request.method == 'POST':
		state = request.form['state']
		params = request.form['params']
		message_queue.put({'state':state,'params':params})
	else:
		return render_template('index.html')

STOP = "stop"

def main_loop(strip, message_queue):
	led_map = [
		list(range(0,37)),
		list(range(75,36,-1)),
		list(range(85,122)),
		list(range(158,121,-1)),
	]
	state = 'meteors'	
	params = None
	led_state = State(led_map,strip)
	meteors = Meteors(led_state)
	rainbowy = Rainbowy(led_state)
	while True:
		if not message_queue.empty():
			msg = message_queue.get()
			if msg == STOP:
				break
			else:
				state = msg[0]
				params = msg[1]
		if state == 'meteors':
			meteors.step()
		elif state == 'rainbowy':
			rainbowy.step()
		else:
			if led_state.any_on():
				led_state.map_all(lambda c: tuple([max(x-15,0) for x in c]))
			else:
				# Save energy by sleeping a bit
				time.sleep(0.5)
			
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
		#	rainbowCycle(strip)
		state.show()
def startup():
	print("init")
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)

	thread = Thread(target=main_loop,args=(strip,message_queue))

	def signal_handler(signal, frame):
		print("stop")
		message_queue.put(STOP)
		colorWipe(strip, Color(0,0,0), wait_ms=1)
		thread.join()
		sys.exit(0)
	signal.signal(signal.SIGINT, signal_handler)
	signal.signal(signal.SIGTERM, signal_handler)

	# Create NeoPixel object with appropriate configuration.
	# Intialize the library (must be called once before other functions).
	strip.begin()
	thread.start()

startup()
