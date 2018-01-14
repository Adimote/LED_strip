def random_brightness(c):
        brightness_factor = random.random()*2+0.8
        return tuple([i*brightness_factor for i in c])

def wheel(pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
                return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
                pos -= 85
                return Color(255 - pos * 3, 0, pos * 3)
        else:
                pos -= 170
                return Color(0, pos * 3, 255 - pos * 3)

def wheel_c(pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
                return (pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
                pos -= 85
                return (255 - pos * 3, 0, pos * 3)
        else:
                pos -= 170
                return (0, pos * 3, 255 - pos * 3)


def color_maxed(c):
        c2 = tuple([max(min(int(round(i)),255),0) for i in c])
        return Color(c2[0],c2[1],c2[2])

def interpolate(colors, row, offset=0):
        spaces = np.linspace(0,len(row)*2,len(colors)*2-1)
        all_colors = colors+colors[:-1][::-1]
        interp = interp1d(spaces,all_colors,axis=0)
        return [(color_maxed(interp((i+offset) % (2*len(row)))),l) for i,l in enumerate(row)]

led_map = [
list(range(0,37)),
list(range(75,36,-1)),
list(range(85,122)),
list(range(158,121,-1)),
]

led_map_and_index = [[(l,(x,y)) for y,l in enumerate(row)] for x,row in enumerate(led_map)]

led_colors = [[(0,0,0) for _ in row] for row in led_map]

purple = [100,0,220]
green = [0,255,0]
red = [255,0,0]
blue = [0,0,255]
orange = [255,140,0]
white = [255,255,255]

