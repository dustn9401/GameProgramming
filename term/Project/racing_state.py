import pico2d
import game_framework
import random
import math
import json
import base
import background
import garage_state
import time
#WIDTH, HEIGHT = pico2d.get_canvas_width(), pico2d.get_canvas_height()    #window size
WIDTH, HEIGHT = 800, 600
MAX_LEV = 5     #max level
MAX_INT_LENGTH = 10

LEFT, RIGHT, UP, STOP, DEAD = range(5)    #car state
NUM_CAR = 20
NUM_TREE = 100
ROAD_L, ROAD_R = 100, 700
DELAY=0.01      #draw 시 delay함수 호출, accel, dir 변수 함께 조정

# =============== 코인, 속도, 숫자 표시 관련 =====================
class Number(base.BaseObject):
    image = None
    WIDTH, HEIGHT = 44, 58
    def __init__(self, x, y):
        self.x, self.y = x, y
        if Number.image == None:
            Number.image = pico2d.load_image('res/img/numbers.png')
            print('Number', self.image)
    def draw(self, num):
        Number.image.clip_draw(num*self.WIDTH, 0, self.WIDTH, self.HEIGHT, self.x, self.y)
    def update(self):
        pass
class Numbers(base.BaseObject):
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.num = 0
        self.numbers = [Number(self.x + i*Number.WIDTH, self.y) for i in range(MAX_INT_LENGTH)]
        self.WIDTH = 44 * len(str(self.num))
        self.HEIGHT = 58
    def draw(self):
        string = str(self.num)
        for i in range(len(string)):
            self.numbers[i].draw(int(string[i]))
    def update(self):        
        for n in self.numbers: n.update()
class Info(base.BaseObject):
    WIDTH, HEIGHT = 100, 100
    def __init__(self):
        self.x, self.y = 500, 500
        self.coin = Coin(self.x, self.y)
        self.coin_numbers = Numbers(self.x + Coin.WIDTH, self.y)
    def draw(self):
        self.coin.draw()
        self.coin_numbers.draw()
    def update(self):
        global player
        self.coin.update()
        self.coin_numbers.num = player.coin
        self.coin.x, self.coin.y = self.x, self.y
        
#======================= 차 그리기 ======================

class Car(base.BaseObject):
    images = [None for i in range(MAX_LEV)]
    def __init__(self, level):
        self.x = random.randint(ROAD_L + 100, ROAD_R - 100)
        self.y = random.randint(0, HEIGHT)
        self.accel = 0
        self.dir = 0
        self.level = level
        self.max_speed = garage_state.car_info[self.level - 1]['speed']
        self.y_speed = random.uniform(1.0, self.max_speed)
        self.x_speed = 200*DELAY*math.log2(self.level+1)
        self.state = STOP
        self.frame = 0
        self.max_frame = 8
        self.image = None
        if Car.images[self.level] == None:
            Car.images[self.level] = pico2d.load_image('res/img/lv_%d.png'%self.level)
        self.image = Car.images[self.level]
        self.WIDTH = self.image.w
        self.HEIGHT = self.image.h // self.max_frame
    def draw(self):
        self.image.clip_draw(0, self.frame*(self.image.h//self.max_frame), self.image.w, self.image.h//self.max_frame, self.x, self.y)
        self.drawRect()
        #clip_composite_draw(self.frame*100, 300, 100, 100, math.pi/2, '', self.x, self.y, 100, 100)
    def update(self):
        global player, bg
        if self.state == DEAD:
            self.reset()
        # ============= 좌표 업데이트 ==============
            
        self.x_speed = 200*DELAY*self.dir*math.log2(self.level+1)
        self.x = pico2d.clamp(100-bg.road.x, self.x + self.x_speed, bg.road.image.w - bg.road.x - 100)
        
        self.y_speed = pico2d.clamp(-self.max_speed, self.y_speed + self.accel, self.max_speed)      #속도 += 가속도
        self.y -= (player.car.y_speed - self.y_speed)
        
        if self.y < -100 or self.y > HEIGHT + 200:
            self.reset()

        # ============= 상태 업데이트 ==============
        if self.y_speed == 0:
            self.state = STOP
        elif self.dir == 1:
            self.state = RIGHT
        elif self.dir == -1:
            self.state = LEFT
        else:
            self.state = UP    
        self.frame = (self.frame + 1) % self.max_frame
    def reset(self):
        self.x = random.randint(ROAD_L+100, ROAD_R-100)
        self.y = 0-100 if random.randint(0,1) else HEIGHT+100
        self.x_speed = 0
        self.y_speed = random.uniform(1.0, self.max_speed)
        
class Explosion(base.BaseObject):
    image = None
    WIDTH, HEIGHT = 128, 128
    FRAME_SIZE = 16
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.frame = 0
        if Explosion.image == None:
            Explosion.image = pico2d.load_image('res/img/Explosion.png')
            print('Explosion', Explosion.image)
        self.st, self.ed = time.time(), 0
        self.end = False
    def draw(self):
        Explosion.image.clip_draw((self.frame%4)*self.WIDTH, (self.frame//4)*self.HEIGHT, self.WIDTH, self.HEIGHT, self.x, self.y)
    def update(self):
        global player
        self.ed = time.time()
        if self.ed - self.st > 0.05: 
            self.frame += 1
            self.st = self.ed
        if self.frame > Explosion.FRAME_SIZE:
            self.end = True
class Death(base.BaseObject):
    images = [None for i in range(MAX_LEV)]
    def __init__(self, x, y, lev):
        self.x, self.y = x, y
        self.frame = 0
        self.level = lev
        self.max_frame = 0
        if self.level == 1: 
            self.max_frame = 8
        else:
            self.max_frame = 7
        if Death.images[self.level] == None:
            Death.images[self.level] = pico2d.load_image('res/img/dead_lv%d.png'%self.level)
        self.image = Death.images[self.level]
        self.WIDTH, self.HEIGHT = self.image.w, self.image.h
        self.st, self.ed = time.time(), 0
        self.end = False
    def draw(self):
        if self.level == 1:
            self.image.clip_draw(0, (self.max_frame - self.frame - 1)*(self.image.h//self.max_frame), self.image.w, self.image.h//self.max_frame, self.x, self.y)
        else:
            self.image.clip_draw(self.frame*self.image.w//self.max_frame, 0, self.image.w//self.max_frame, self.image.h, self.x, self.y)
    def update(self):
        global player
        self.ed = time.time()
        if self.ed - self.st > 0.1: 
            self.frame += 1
            self.st = self.ed
        if self.frame > self.max_frame:
            self.end = True
class Coin(base.BaseObject):
    image = None
    WIDTH, HEIGHT = 50, 50
    FRAME_SIZE = 10
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.frame = 0
        self.speed = 10
        self.end = False
        if Coin.image == None:
            Coin.image = pico2d.load_image('res/img/coin.png')
            print('Coin', self.image)
    def draw(self):
        Coin.image.clip_draw(self.frame*self.WIDTH, 0, self.WIDTH, self.HEIGHT, self.x, self.y)
        #self.image.clip_composite_draw(self.frame*100, 300, 100, 100, math.pi/2, '', self.x, self.y, 100, 100)
    def update(self):
        global info
        self.frame = (self.frame + 1) % self.FRAME_SIZE
        dx, dy = info.coin.x - self.x, info.coin.y - self.y
        arctan = math.atan2(dy, dx)
        self.x += self.speed*math.cos(arctan)
        self.y += self.speed*math.sin(arctan)
        dx = (self.x - info.coin.x)
        dy = (self.y - info.coin.y)
        if dx*dx + dy*dy < 100:
            self.end = True
            
        
class Player(base.BaseObject):
    endl = False
    def __init__(self):
        global player_data
        self.coin = player_data['player']['coin']
        self.level = player_data['player']['level']
        self.car = Car(self.level)
        self.car.x = WIDTH//2
        self.car.y = HEIGHT//4
        self.car.y_speed = 0
        self.dx = 0
    def draw(self):
        self.car.draw()
    def update(self):
        global player_data, bg, cars
        
        tx = self.car.x
        self.car.update()
        self.dx = self.car.x - tx
        player_data['player']['coin'] = self.coin
        player_data['player']['level'] = self.level
        
def handle_events():
    global road, player
    events = pico2d.get_events()
    for e in events:
        if e.type == pico2d.SDL_QUIT:
            game_framework.quit()
        elif e.type == pico2d.SDL_KEYDOWN:
            if e.key == pico2d.SDLK_ESCAPE:
                game_framework.pop_state()
            elif e.key == pico2d.SDLK_LEFT:
                player.car.dir -= 1
            elif e.key == pico2d.SDLK_RIGHT:
                player.car.dir += 1
            elif e.key == pico2d.SDLK_DOWN:
                player.car.accel -= DELAY*10*math.log2(player.car.level + 1)
            elif e.key == pico2d.SDLK_UP:
                player.car.accel += DELAY*10*math.log2(player.car.level + 1)
        elif e.type == pico2d.SDL_KEYUP:
            if e.key == pico2d.SDLK_LEFT:
                player.car.dir += 1
            elif e.key == pico2d.SDLK_RIGHT:
                player.car.dir -= 1
            elif e.key == pico2d.SDLK_UP:
                player.car.accel -= DELAY*10*math.log2(player.car.level + 1)
            elif e.key == pico2d.SDLK_DOWN:
                player.car.accel += DELAY*10*math.log2(player.car.level + 1)

def checkRect(r1, r2):
    if r1[0][0] > r2[1][0] or r1[0][1] > r2[1][1] or r1[1][0] < r2[0][0] or r1[1][1] < r2[0][1]:
        return False
    return True
def collision_check():
    global player, cars, coins, fires
    pRect = player.car.getRect()
    for c in cars:
        if checkRect(pRect, c.getRect()):
            c.state = DEAD
            if c.level <= 4:
                fires.append(Death(c.x, c.y, c.level))
            else:
                fires.append(Explosion(c.x, c.y))
            for i in range(c.level):    #터트린 차량의 레벨에 비례한 코인 생성
                coins.append(Coin(c.x + random.randint(-20, 20), c.y + random.randint(-20, 20))) 
            player.coin += c.level
def load_data():
    global player_data
    with open('res/player_data.json', 'r') as fp:
        player_data = json.load(fp)
def save_data():
    global player_data
    with open('res/player_data.json', 'w') as fp:
        json.dump(player_data, fp)
def enter():
    global player, cars, coins, info, fires, player_data, bg
    load_data()    
    fires = []
    info = Info()
    coins = []
    player = Player()
    cars = []
    for i in range(NUM_CAR):
        cars.append(Car(random.randrange(1,MAX_LEV)))
    bg = background.Background()

def exit():
    global bg, player, cars, coins, fires, info
    save_data()
    del player, bg, cars, coins, fires, info

def draw():
    global bg, player, cars, coins, fires
    pico2d.clear_canvas()
    bg.draw()
    for c in cars:
        c.draw()
    for c in coins:
        c.draw()
    for f in fires:
        f.draw()
    player.draw()
    for c in bg.clouds:
        c.draw()
    info.draw()
    pico2d.update_canvas()
    pico2d.delay(DELAY)

def update():
    global bg, player, cars, coins, fires, info
    bg.update()   #도로 업데이트
    collision_check()       #충돌체크
    player.update()     #플레이어 차 업테이트
    for c in cars:
        c.update()          #상대 차들 업데이트
        if random.randint(0, 100) == 0:
#            pass
            c.dir = random.randint(-1, 1)
            
    for i,f in enumerate(fires):
        f.update()
        if f.end: del fires[i]
    for i,c in enumerate(coins):
        c.update()
        if c.end: del coins[i]
        
    bg.update()
    info.update()
def pause():
    pass
def resume():
    pass

def main():
    pico2d.open_canvas()
    running = True
    enter()
    while running:
        handle_events()
        update()
        draw()
    exit()
    pico2d.close_canvas()

if __name__ == '__main__':
    main()
