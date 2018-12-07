import pico2d
import game_framework
import garage_state
import racing_state
import base
import ui
import time
cw = 800
ch = 600
gameover = None
earn_coin = 0
live_time = 0
def onClick(context):
    global player
    if context == 'restart':
        racing_state.start_time = time.time()
        racing_state.earn_coin = 0
        game_framework.change_state(racing_state)
    if context == 'before':
        game_framework.change_state(garage_state)

class Gameover:
    def __init__(self):
        self.btn_start = ui.Button('res/img/racestart', 600, 100, onClick, 'racestart')
        self.btn_buy = ui.Button('res/img/buy', 600, 100, onClick, 'buy')
        self.btn = [\
            ui.Button('res/img/before', 200, 300, onClick, 'before'),\
            ui.Button('res/img/restart', 600, 300, onClick, 'restart'),\
            ]
        self.lbl = [\
            ui.Label('Game Over', 200, 500, 100, ui.FONT_2),\
            ui.Label('살아남은 시간: %.3f 초'%live_time, cw//2, 200, 30, ui.FONT_2),\
            ui.Label('획득한 코인: %d$'%earn_coin, cw//2, 150, 30, ui.FONT_2),\
            ]
    def update(self):
        ui.buttons = self.btn
        ui.labels = self.lbl
        ui.update()
    def draw(self):
        ui.draw()
            

def handle_events():
    events = pico2d.get_events()
    for e in events:
        if e.type == pico2d.SDL_QUIT:
            game_framework.quit()
        ui.handle_event(e)
                    
def enter():
    global gameover
    gameover = Gameover()

def exit():
    global gameover
    del gameover

def pause():
    pass
def resume():
    pass

def draw():
    global gameover
    pico2d.clear_canvas()
    gameover.draw()
    pico2d.update_canvas()

def update():
    global gameover
    gameover.update()

