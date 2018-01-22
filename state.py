from neopixel import Color
def color_limited(c):
        return tuple([max(min(int(round(i)),255),0) for i in c])

class State(object):
	def __init__(self, mapping, strip):
		"""
			Create a mapping of LEDs given a 2D array.
		"""
		self.width = max([len(row) for row in mapping])
		self.height = len(mapping)
		self.led_colors = [[(0,0,0) for _ in row] for row in mapping]
		self.positions = [[(x,y) for y,_ in enumerate(row)] for x,row in enumerate(mapping)]
		self._led_map = mapping
		self.strip = strip
	
	def map_all(self,func):
		"""
			Run the given function on all LEDs
		"""
		for x,row in enumerate(self._led_map):
			for y,_ in enumerate(row):
				self[x,y] = func(self[x,y])
	def any_on(self):
		""" Return if any LEDs are on """
		for x,row in enumerate(self.led_colors):
			for y,c in enumerate(row):
				if color_limited(c) != (0,0,0):
					return True
		return False
	
	def __getitem__(self,pos):
		x,y = pos
		return self.led_colors[x][y]

	def __setitem__(self,pos,color):
		x,y = pos
		new_color = color_limited(color)
		if any([c1 != c2 for c1,c2 in zip(new_color,self[x,y])]):
			self.strip.setPixelColor(self._led_map[x][y],
				Color(new_color[0], new_color[1], new_color[2]))
		self.led_colors[x][y] = color
	
	def __len__(self):
		return sum([len(row) for row in self._led_map])

	def row(self,i):
		return self.led_colors[i]

	def col(self,i):
		return [row[i] for row in self.led_colors]

	def show(self):
		self.strip.show()
