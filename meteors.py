import time
import random
from common import add_color,wheel,random_brightness

class Meteors:

	def __init__(self,state):
		self.meteors = []
		self.cooldown = 0
		self.state = state

	def add_meteor(self,pos,color):
		self.meteors.append((color,pos))

	def step(self,wait_ms=5):
		self.state.map_all(lambda _, c: tuple([max(x-15,0) for x in c]))
		self.cooldown -= 1
		if random.random() < 0.05 and self.cooldown <= 0:
			self.cooldown = 20
			direction = random.choice([-1,1])
			shelves = [
				[self.state.positions[0],self.state.positions[1]],
				[self.state.positions[2],self.state.positions[3]],
			]
			shelf = random.choice(shelves)
			self.add_meteor(shelf[0][::direction],wheel(random.randint(0,255)))
			self.add_meteor(shelf[1][::direction],wheel(random.randint(0,255)))
		for color,leds in self.meteors:
			if not leds:
				self.meteors.remove((color,leds))
				continue
			led = leds.pop()
			x,y = led
			# set color
			self.state[x,y] = add_color(random_brightness(color),self.state[x,y])
		time.sleep(wait_ms/1000.0)
