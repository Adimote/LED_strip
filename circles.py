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

