import pico2d
import game_framework
import racing_state
import base
import ui
MAX_LEV = 4
car_info = {\
            0: {'name': '사람', 'speed': 10},\
            1: {'name': '강아지', 'speed': 15},\
            2: {'name': '프레데터', 'speed': 20},\
            3: {'name': '귀신', 'speed': 25},\
        }
def onClick(context):
    global garage
    if context == 'racestart': 
        game_framework.push_state(racing_state)
    if context == 'before':
        game_framework.pop_state()
    if context == 'la':
        if garage.slot[0] > 0:
            garage.slot = [x-1 for x in garage.slot]
    if context == 'ra':
        if garage.slot[2] < MAX_LEV - 1:
            garage.slot = [x+1 for x in garage.slot]
    if context == 's1':
        garage.select = 0
    if context == 's2':
        garage.select = 1
    if context == 's3':
        garage.select = 2
class Garage:
    def __init__(self):
        self.btn = [\
                ui.Button('res/img/racestart', 600, 100, onClick, 'racestart'),\
                ui.Button('res/img/before', 200, 100, onClick, 'before'),\
                ui.Button('res/img/left_arrow', 50, 500, onClick, 'la'),\
                ui.Button('res/img/right_arrow', 750, 500, onClick, 'ra'),\
                ui.Button('res/img/slot', 200, 500, onClick, 's1'),\
                ui.Button('res/img/slot', 400, 500, onClick, 's2'),\
                ui.Button('res/img/slot', 600, 500, onClick, 's3'),\
                ]
        self.lbl = []
        self.slot = [0, 1, 2]
        self.slot_imgs = [pico2d.load_image('res/img/slot_lv%d.png'%(i+1)) for i in range(MAX_LEV)]
        self.select = None
    def update(self):
        ui.buttons = self.btn
        ui.labels = self.lbl
        ui.update()
        if self.select != None:
            self.lbl = [\
                    ui.Label('이름: ' + car_info[self.slot[self.select]]['name'], 400, 300, 50, ui.FONT_3),\
                    ui.Label('최고속력: ' + str(car_info[self.slot[self.select]]['speed']) + 'km/s', 400, 230, 50, ui.FONT_2),\
                    ]
    def draw(self):
        ui.draw()
        self.slot_imgs[self.slot[0]].draw(200, 500)
        self.slot_imgs[self.slot[1]].draw(400, 500)
        self.slot_imgs[self.slot[2]].draw(600, 500)
        
        if self.select != None:
            img = self.slot_imgs[self.slot[self.select]]
            img.clip_draw(0,0,img.w,img.h,200,300,200,200)
            

def handle_events():
    global garage
    events = pico2d.get_events()
    for e in events:
        if e.type == pico2d.SDL_QUIT:
            game_framework.quit()
        elif e.type == pico2d.SDL_KEYDOWN:
            if e.key == pico2d.SDLK_ESCAPE:
                game_framework.pop_state()
            if e.key == pico2d.SDLK_SPACE:
                game_framework.push_state(racing_state)
        ui.handle_event(e)
                    
def enter():
    global garage
    garage = Garage()

def exit():
    global garage
    del garage

def pause():
    pass
def resume():
    pass

def draw():
    global garage
    pico2d.clear_canvas()
    garage.draw()
    pico2d.update_canvas()

def update():
    global garage
    garage.update()

