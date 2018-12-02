import pico2d
import game_framework
import racing_state
import base
import ui
import json
MAX_LEV = 5
garage = None
data = {}
with open('res/player_data.json', 'r') as fp:
    data = json.load(fp)
player_info = data['player']
car_info = data['car_info']
def save_data():
    global data
    with open('res/player_data.json', 'w') as fp:
        data['player'] = player_info
        data['car_info'] = car_info
        json.dump(data, fp)
def onClick(context):
    global garage, player_info
    if context == 'racestart':
        game_framework.push_state(racing_state)
    if context == 'buy':
        have = player_info['coin']
        cost = car_info[str(garage.slot[garage.select])]['cost']
        if have >= cost:
            player_info['coin'] -= cost
            player_info['level'] += 1
            player_info['have'].append(garage.slot[garage.select])
            save_data()
        else:
            pass
    if context == 'before':
        game_framework.pop_state()
    if context == 'la':
        if garage.slot[0] > 0:
            garage.slot = [x-1 for x in garage.slot]
    if context == 'ra':
        if garage.slot[2] < MAX_LEV - 1:
            garage.slot = [x+1 for x in garage.slot]
    if context[0] == 's' and len(context) == 2:
        if context == 's1':
            garage.select = 0
        if context == 's2':
            garage.select = 1
        if context == 's3':
            garage.select = 2
class Coin(base.BaseObject):
    image = None
    WIDTH, HEIGHT = 50, 50
    FRAME_SIZE = 10
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.frame = 0
        if Coin.image == None:
            Coin.image = pico2d.load_image('res/img/coin.png')
    def draw(self):
        Coin.image.clip_draw(self.frame*self.WIDTH, 0, self.WIDTH, self.HEIGHT, self.x, self.y)
    def update(self):
        self.frame = (self.frame + 1) % self.FRAME_SIZE
class Garage:
    lock = None
    def __init__(self):
        if Garage.lock == None:
            Garage.lock = pico2d.load_image('res/img/lock.png')
        self.slot = [0, 1, 2]
        self.slot_imgs = [pico2d.load_image('res/img/slot_lv%d.png'%(i+1)) for i in range(MAX_LEV)]
        self.select = 0
        self.coin = Coin(380, 400)
        self.p_lev = player_info['level']
        self.msg = '탑승가능'
        self.able = True
        self.btn_start = ui.Button('res/img/racestart', 600, 100, onClick, 'racestart')
        self.btn_buy = ui.Button('res/img/buy', 600, 100, onClick, 'buy')
        self.btn = [\
                self.btn_start,\
                ui.Button('res/img/before', 200, 100, onClick, 'before'),\
                ui.Button('res/img/left_arrow', 50, 500, onClick, 'la'),\
                ui.Button('res/img/right_arrow', 750, 500, onClick, 'ra'),\
                ui.Button('res/img/slot', 200, 500, onClick, 's1'),\
                ui.Button('res/img/slot', 400, 500, onClick, 's2'),\
                ui.Button('res/img/slot', 600, 500, onClick, 's3'),\
                ]
        self.lbl = []
    def update(self):
        self.lbl = [\
                    ui.Label('가진 돈: %d'%player_info['coin'] + '$', 400, 400, 30, ui.FONT_3),\
                    ui.Label('이름: ' + car_info[str(self.slot[self.select])]['name'], 400, 370, 30, ui.FONT_3),\
                    ui.Label('최고속력: %d'%car_info[str(self.slot[self.select])]['speed'] + 'km/s', 400, 340, 30, ui.FONT_2),\
                    ui.Label('가격: %d'%car_info[str(self.slot[self.select])]['cost'] + '$', 400, 310, 30, ui.FONT_2),\
                    ui.Label(self.msg, 400, 280, 30, ui.FONT_2),\
                    ]
        if self.slot[self.select] in player_info['have']:
            self.btn[0] = self.btn_start
            self.msg = '탑승가능'
        else:
            self.btn[0] = self.btn_buy
            have = player_info['coin']
            cost = car_info[str(garage.slot[garage.select])]['cost']
            if have < cost:
                self.msg = '돈이 부족합니다!!'
            else:
                self.msg = '차량이 잠겨있습니다!!'
            
        ui.buttons = self.btn
        ui.labels = self.lbl
        ui.update()
        self.coin.update()
    def draw(self):
        ui.draw()
        self.coin.draw()
        self.slot_imgs[self.slot[0]].draw(200, 500)
        self.slot_imgs[self.slot[1]].draw(400, 500)
        self.slot_imgs[self.slot[2]].draw(600, 500)
        if self.slot[0] not in player_info['have']:
            self.lock.draw(200, 500)
        if self.slot[1] not in player_info['have']:
            self.lock.draw(400, 500)
        if self.slot[2] not in player_info['have']:
            self.lock.draw(600, 500)
        
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

