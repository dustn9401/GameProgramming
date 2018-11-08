from pico2d import *
import game_world
import config
import boys_state
import math
class Bong:
    image = None
    canvas_width = 0
    canvas_height = 0
    def __init__(self):
        if Bong.image == None:
            Bong.image = load_image('../res/bong.png')
        if Bong.canvas_width == 0:
            Bong.canvas_width = get_canvas_width()
            Bong.canvas_height = get_canvas_height()
        self.x, self.y = 0, 0
        self.angle = 0
        self.power = 0
    def draw(self):
        self.image.composite_draw(self.angle, '', self.x, self.y, 200, 200)
    def update(self):
        self.x = boys_state.boy.x
        self.y = boys_state.boy.y

        mx, my = boys_state.mx, boys_state.my
        dx = mx - self.x
        dy = my - self.y
        self.power = (dx**2 + dy**2)/1000
        self.angle = math.atan2(dy, dx)

       
