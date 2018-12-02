#import pico2d
#import sys
import time
#
#pico2d.open_canvas()
#road = pico2d.load_image('res/road.png')
#
#while True:
#    events = pico2d.get_events()
#    for e in events:
#        if e.type == pico2d.SDL_QUIT:
#            pico2d.close_canvas()
#            sys.exit(1)
#    pico2d.clear_canvas()
#    road.clip_draw_to_origin(0, 0, 800, 600, 0, 0)
#    #road.clip_draw(0, 0, 300, 300, 10, 10)
#    pico2d.update_canvas()

t = time.time()
for _ in range(100000):
    a = 10
ela = time.time() - t

a = 0.012
b = 0.56
print(b%a)