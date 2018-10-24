from sense_hat import SenseHat 
import math 
import time
from copy import copy

ADJUST = 0.5
MIN_PERIOD = 3
MAX_PERIOD = MIN_PERIOD + ADJUST*7

s = SenseHat()
# linear gamma means we actually get brightnesses lower than 50
s.gamma = [i for i in range(32)]

def clamp(value, min_value=0, max_value=7):
    return min(max_value, max(min_value, value))

def delta(direction):
    return {
        "up": 1,
        "down": -1
    }[direction] 

def event_delta(event):
    return delta(event.direction)

def control(e, p, k, r, mi, ma):
    if (e.direction in ["up", "down"] and 
        e.action in ["released", "held"]):
        setattr(p, k, clamp(getattr(p, k) + r * event_delta(e), mi, ma))
        return True
    return False

def handle_events(p):
    p = copy(p)
    for e in s.stick.get_events():
        modified = control(e, p, 'period', 0.5, MIN_PERIOD, MAX_PERIOD) 
        if modified:
            p.show_period = p.ticks
            p.j = 0
        if (e.direction == "middle" and e.action == "pressed"):
            p = Params()
    return p

class Params():
    def __init__(self):
        self.j = 0
        self.fps = 60
        self.sleep = 1/self.fps
        self.period = 4
        self.ticks = self.period/self.sleep
        self.wave_depth = 3.5
        self.tide = 0.25
        self.show_period = 0

def main():
    p = Params()
    while True:
        p = handle_events(p) 
        p.ticks = p.period/p.sleep
        for i in range(0, 64):
            x = i % 8
            y = int(i / 8)
            wave_height = int(8 * (1 - (1 + math.cos(
                2*math.pi*(
                    (p.j/p.ticks)
                    + 0.10*(1 - (1 + math.cos(2*math.pi*(x/7)))/2)
                )
            )) /2))
            brightness = clamp((wave_height-y+1)/7, 0, 1)
            r = math.sin(2*math.pi*(p.j/(p.ticks*16)) + 0) * 127 + 128
            g = math.sin(2*math.pi*(p.j/(p.ticks*16)) + 2*math.pi/3) * 127 + 128
            b = math.sin(2*math.pi*(p.j/(p.ticks*16)) + 4*math.pi/3) * 127 + 128
            s.set_pixel(x, (7 - y), (
                int(brightness*r),
                int(brightness*g),
                int(brightness*b)))
            if p.show_period > 0:
                p.show_period -= 1
                for i in range(0, int(8*((1+p.period-MIN_PERIOD)/(1+MAX_PERIOD-MIN_PERIOD)))):
                    v = int(255 - (i+1/8))
                    s.set_pixel(i, 7, (v, v, v))
                    
        time.sleep(p.sleep)
        p.j += 1

if __name__ == '__main__':
    main()
