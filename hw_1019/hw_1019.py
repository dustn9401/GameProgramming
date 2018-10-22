import pico2d
import math
import random
IDLE, RUN, SLEEP = range(3)

class Grass:
    def __init__(self):
        self.image = pico2d.load_image('../res/grass.png')
        print(self.image)
    def draw(self):
        self.image.draw(400, 30)

class Boy:
    image = None
    def __init__(self):
        print("Creating..")
        self.x = random.randint(100, 700)
        self.y = 90
        self.speed = 3
        self.frame = random.randint(0, 7)
        self.timer = 0
        self.velocity = 0
        self.event_que=[]
        self.cur_state = IDLE
        self.dir = 1
        self.enter_state[IDLE](self)
        if Boy.image == None:
            Boy.image = pico2d.load_image('../res/animation_sheet.png')

    def enter_SLEEP(self):
        self.frame = 0
    def exit_SLEEP(self):
        pass
    def do_SLEEP(self):
        self.frame = (self.frame + 1)%8
    def draw_SLEEP(self):
        if self.dir == 1:
            Boy.image.clip_composite_draw(self.frame*100, 300, 100, 100, math.pi/2, '', self.x, self.y, 100, 100)
        else:
            Boy.image.clip_composite_draw(self.frame*100, 200, 100, 100, -math.pi/2, '', self.x, self.y, 100, 100)
    def enter_IDLE(self):
        self.timer =100
        self.frame =0
    def exit_IDLE(self):
        pass
    def do_IDLE(self):
        self.frame = (self.frame + 1)%8
        self.timer -= 1
        if self.timer == 0:
            self.change_state(SLEEP)
    def draw_IDLE(self):
        if self.dir == 1:
            Boy.image.clip_draw(self.frame * 100, 300, 100, 100, self.x, self.y)
        else:
            Boy.image.clip_draw(self.frame * 100, 200, 100, 100, self.x, self.y)
    def enter_RUN(self):
        self.frame = 0
        self.dir = self.velocity
    def exit_RUN(self):
        pass
    def do_RUN(self):
        self.frame = (self.frame + 1)%8
        self.x += self.velocity
        self.x = pico2d.clamp(25, self.x, 800-25)
    def draw_RUN(self):
        if self.velocity == 1:
            Boy.image.clip_draw(self.frame * 100, 100, 100, 100, self.x, self.y)
        else:
            Boy.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)

    enter_state = {IDLE: enter_IDLE, RUN: enter_RUN, SLEEP: enter_SLEEP}
    exit_state = {IDLE: exit_IDLE, RUN: exit_RUN, SLEEP: exit_SLEEP}
    do_state = {IDLE: do_IDLE, RUN: do_RUN, SLEEP: do_SLEEP}
    draw_state = {IDLE: draw_IDLE, RUN: draw_RUN, SLEEP: draw_SLEEP}

    def draw(self):
        self.draw_state[self.cur_state](self)
    def update(self):
        self.do_state[self.cur_state](self)
    def change_state(self, state):
        self.exit_state[self.cur_state](self)
        self.enter_state[state](self)
        self.cur_state = state
    def add_event(self, event):
        self.event_que.insert(0, event)

def handle_events():
    global running, boy
    events = pico2d.get_events()
    for event in events:
        if event.type == pico2d.SDL_QUIT:
            running = False
        elif event.type == pico2d.SDL_KEYDOWN:
            if event.key == pico2d.SDLK_ESCAPE:
                running = False
            elif event.key == pico2d.SDLK_RIGHT:
                boy.velocity += 1
                boy.change_state(RUN)
            elif event.key == pico2d.SDLK_LEFT:
                boy.velocity -= 1
                boy.change_state(RUN)
        elif event.type == pico2d.SDL_KEYUP:
            if event.key == pico2d.SDLK_RIGHT:
                boy.velocity -= 1
                boy.change_state(IDLE)
            elif event.key == pico2d.SDLK_LEFT:
                boy.velocity += 1
                boy.change_state(IDLE)
            
pico2d.open_canvas()
grass = Grass()
boy = Boy()

running = True
while running:
    pico2d.clear_canvas()
    grass.draw()
    boy.update()
    boy.draw()
    print('timer = %d'%boy.timer)
    pico2d.update_canvas()
    handle_events()
    pico2d.delay(0.01)

pico2d.close_canvas()
