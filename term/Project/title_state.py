import pico2d
import game_framework
import garage_state
import base
import ui
def onClick(context):
    if context == 'gamestart': 
        game_framework.push_state(garage_state)
class Title:
    def __init__(self):
        self.btn = [\
                    ui.Button('res/img/gamestart', 500, 100, onClick, 'gamestart'),\
                ]
        self.image = pico2d.load_image('res/img/title.png')
        print('Title', self.image)
    def update(self):
        ui.buttons = self.btn
        ui.update()
    def draw(self):
        self.image.draw(400, 300)
        ui.draw()
def handle_events():
    global title
    events = pico2d.get_events()
    for e in events:
        if e.type == pico2d.SDL_QUIT:
            game_framework.quit()
        elif e.type == pico2d.SDL_KEYDOWN:
            if e.key == pico2d.SDLK_ESCAPE:
                game_framework.quit()
            if e.key == pico2d.SDLK_SPACE:
                game_framework.push_state(garage_state)
        ui.handle_event(e)

def enter():
    global title
    title = Title()

def exit():
    global title
    del title

def pause():
    pass
def resume():
    pass

def draw():
    global title
    pico2d.clear_canvas()
    title.draw()
    pico2d.update_canvas()

def update():
    global title
    title.update()