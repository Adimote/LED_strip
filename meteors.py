

class Meteors(object):

	def __init__(self,strip,led_colors):
		self.meteors = []
		self.cooldown = 0
		self.strip = strip

	def add_meteor(leds,color):
		meteor = (color, leds)
		self.meteors.append(meteor)

	def add_color(x,y,color):
		self.led_colors[x][y] = tuple([old+new for new,old in zip(color,led_colors[x][y])])
			

	def step(wait_ms=5):
		map_all(self.strip,lambda c: tuple([max(x-15,0) for x in c]))
		self.cooldown -= 1
		if random.random() < 0.05 and cooldown <= 0:
			cooldown = 20
			direction = random.choice([-1,1])
			shelves = [[led_map_and_index[0],led_map_and_index[1]],[led_map_and_index[2],led_map_and_index[3]]]
			shelf = random.choice(shelves)
			add_meteor(shelf[0][::direction],wheel_c(random.randint(0,255)))
			add_meteor(shelf[1][::direction],wheel_c(random.randint(0,255)))
		for color,leds in self.meteors:
			if not leds:
				self.meteors.remove((color,leds))
				continue
			led = leds.pop()
			l,(x,y) = led
			# set color
			add_color(x,y,random_brightness(color))
		self.strip.show()
		time.sleep(wait_ms/1000.0)

			
