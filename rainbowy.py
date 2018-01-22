from common import interpolate, purple, white, orange, red, green, blue

class Rainbowy:

	def __init__(self, state):
		self.state = state
		self.offset = 0

	def step(self):
		self.offset += 1
		x = 0
		colors = [
			interpolate(
				[purple, white],
				len(self.state.positions[0]), self.offset
			),
			interpolate(
				[orange, red],
				len(self.state.positions[1]), self.offset
			),
			interpolate(
				[green, blue],
				len(self.state.positions[2]), self.offset
			),
			interpolate(
				[red, orange],
				len(self.state.positions[3]), self.offset
			),
		]
		for x,row in enumerate(colors):
			for y,c in enumerate(row):
				self.state[x,y] = c

