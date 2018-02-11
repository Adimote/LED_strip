import time
import random
from common import add_color,wheel,random_brightness

RANDOM_THRESH = 0.0002
COLOR = (70,0,0)
DISAPPEAR_DAMPENING = 0.5
APPEAR_DAMPENING = 2

class Coding:


	def __init__(self,state):
		self.dots = set()
		self.state = state
	
	def per_led(self, i, c):
		if i in self.dots:
			if any([c1 != c2 for c1,c2 in zip(c,COLOR)]):
			   return tuple([a+min(max(b-a,-APPEAR_DAMPENING),APPEAR_DAMPENING) for a,b in zip(c,COLOR)])
			else:
			   self.dots.remove(i) 

		if random.random() < RANDOM_THRESH:
			self.dots.add(i)
			return c
		else:
			return tuple([max(x-DISAPPEAR_DAMPENING,0) for x in c])

	def step(self,wait_ms=5):
		self.state.map_all(lambda i, c: self.per_led(i,c))
