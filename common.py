import numpy as np
from scipy.interpolate import interp1d
import random

def random_brightness(c):
        brightness_factor = random.random()*2+0.8
        return tuple([i*brightness_factor for i in c])

def add_color(c1,c2):
	return tuple([old+new for new,old in zip(c1,c2)])

def wheel(pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
                return (pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
                pos -= 85
                return (255 - pos * 3, 0, pos * 3)
        else:
                pos -= 170
                return (0, pos * 3, 255 - pos * 3)

def interpolate(colors, led_count, offset=0):
        spaces = np.linspace(0,led_count*2,len(colors)*2-1)
        all_colors = colors+colors[:-1][::-1]
        interp = interp1d(spaces,all_colors,axis=0)
        return [interp((i+offset) % (2*led_count)) for i in range(led_count)]

purple = [100,0,220]
green = [0,255,0]
red = [255,0,0]
blue = [0,0,255]
orange = [255,140,0]
white = [255,255,255]

