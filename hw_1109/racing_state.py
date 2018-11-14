import pico2d
import game_framework
import random
import math
import json
import base
import bg
#WIDTH, HEIGHT = pico2d.get_canvas_width(), pico2d.get_canvas_height()    #window size
WIDTH, HEIGHT = 800, 600
MAX_LEV = 6     #max level
MAX_SPEEDS = [i*10 for i in range(MAX_LEV)]
MAX_INT_LENGTH = 10

LEFT, RIGHT, UP, STOP, DEAD = range(5)    #car state
NUM_CAR = 0
NUM_TREE = 0
ROAD_L, ROAD_R = 100, 700
DELAY=0.02      #draw 시 delay함수 호출, accel, dir 변수 함께 조정

# =============== 코인, 속도, 숫자 표시 관련 =====================
class Number(base.BaseObject):
    image = None
    WIDTH, HEIGHT = 44, 58
    def __init__(self, x, y):
        self.x, self.y = x, y
        if Number.image == None:
            Number.image = pico2d.load_image('res/numbers.png')
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
        self.x, self.y = 600, 500
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
        
#======================= 나무, 도로, 차 그리기 ======================
#class Tree(base.BaseObject):
#    image = None
#    def __init__(self):
#        self.x = random.randint(0,ROAD_L) if random.randint(0,1) else random.randint(ROAD_R, WIDTH)
#        self.y = random.randint(0, HEIGHT)
#        if Tree.image == None:
#            Tree.image = pico2d.load_image('res/tree.png')
#            print('Tree', self.image)
#    def draw(self):
#        Tree.image.draw(self.x, self.y)
#    def update(self):
#        global player
#        self.y -= player.car.y_speed
#        if self.y < 0: self.y = HEIGHT+200
##class Road(base.BaseObject):
##    WIDTH, HEIGHT = 800, 1534
##    def __init__(self):
##        self.x = WIDTH//2
##        self.y = HEIGHT//2
##        self.image = pico2d.load_image('res/road.png')
##        print('Road', self.image)
##    def draw(self):
##        self.image.draw(self.x, self.y)
##    def update(self):
##        global player
##        self.y -= player.car.y_speed
##        if self.y > self.HEIGHT - 100 or self.y < 100:
##            self.y = 300

class Car(base.BaseObject):
    image = None
    WIDTH, HEIGHT = 46, 62
    def __init__(self, level):
        self.x = random.randint(ROAD_L + 100, ROAD_R - 100)
        self.y = random.randint(0, HEIGHT)
        self.accel = 0
        self.dir = 0
        self.level = level
        self.x_speed = 0
        self.y_speed = random.uniform(1.0, MAX_SPEEDS[self.level])
        self.state = STOP
        self.counter = random.randrange(0,100)
        if Car.image == None:
            Car.image = pico2d.load_image('res/car.png')
            print('Car', Car.image)
    def draw(self):
        Car.image.clip_draw(self.state*self.WIDTH, (self.level-1)*self.HEIGHT, self.WIDTH, self.HEIGHT, self.x, self.y)
        self.drawRect()
        #clip_composite_draw(self.frame*100, 300, 100, 100, math.pi/2, '', self.x, self.y, 100, 100)
    def update(self):
        global player
        if self.state == DEAD:
            self.reset()
        # ============= 좌표 업데이트 ==============
        self.x_speed = 200*DELAY*self.dir*math.log2(self.level+1)
        self.x = pico2d.clamp(100, self.x + self.x_speed, WIDTH - 100)
        self.y_speed = pico2d.clamp(-MAX_SPEEDS[self.level], self.y_speed + self.accel, MAX_SPEEDS[self.level])      #속도 += 가속도
        self.y -= (player.car.y_speed - self.y_speed)        #내 차와의 상대속도만큼 y위치 변경
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
        self.counter = (self.counter + 1)%100
    def reset(self):
        self. x = random.randint(ROAD_L+100, ROAD_R-100)
        self. y = 0-100 if random.randint(0,1) else HEIGHT+100
        self.y_speed = random.uniform(1.0, MAX_SPEEDS[self.level])
    def pos(self):
        return self.x - self.bg.x, self.y - self.bg.y
        
class Explosion(base.BaseObject):
    image = None
    WIDTH, HEIGHT = 128, 128
    FRAME_SIZE = 16
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.frame = 0
        if Explosion.image == None:
            Explosion.image = pico2d.load_image('res/Explosion.png')
            print('Explosion', Explosion.image)
    def draw(self):
        Explosion.image.clip_draw((self.frame%4)*self.WIDTH, (self.frame//4)*self.HEIGHT, self.WIDTH, self.HEIGHT, self.x, self.y)
    def update(self):
        global player
        self.y -= player.car.y_speed
        self.frame += 1
        
class Coin(base.BaseObject):
    image = None
    WIDTH, HEIGHT = 50, 50
    FRAME_SIZE = 10
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.frame = 0
        self.y_speed = 10
        self.x_speed = 10
        if Coin.image == None:
            Coin.image = pico2d.load_image('res/coin.png')
            print('Coin', self.image)
    def draw(self):
        Coin.image.clip_draw(self.frame*self.WIDTH, 0, self.WIDTH, self.HEIGHT, self.x, self.y)
        #self.image.clip_composite_draw(self.frame*100, 300, 100, 100, math.pi/2, '', self.x, self.y, 100, 100)
    def update(self):
        global info
        self.frame = (self.frame + 1) % self.FRAME_SIZE
        dx, dy = info.coin.x - self.x, info.coin.y - self.y
        arctan = math.atan2(dy, dx)
        self.x += self.x_speed*math.cos(arctan)
        self.y += self.y_speed*math.sin(arctan)
        
class Player(base.BaseObject):
    def __init__(self):
        global player_data
        self.coin = player_data['player']['coin']
        self.level = player_data['player']['level']
        self.car = Car(self.level)
        self.x, self.y = self.car.x, self.car.y
    def draw(self):
        self.car.draw()
    def update(self):
        global player_data
        self.car.update()
        player_data['player']['coin'] = self.coin
        player_data['player']['level'] = self.level
        self.x += self.car.x_speed
        self.y += self.car.y_speed
        
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
    global player, cars, road, coins, info, fires, player_data
    load_data()    
    fires = []
    info = Info()
    coins = []
    player = Player()
    player.car.x, player.car.y = 400,200
    cars = []
    for i in range(NUM_CAR):
        cars.append(Car(random.randrange(1,MAX_LEV)))
    road = bg.Background()

def exit():
    global road, player, cars, coins, fires, info
    save_data()
    del player, road, cars, coins, fires, info

def draw():
    global road, player, cars, coins, fires
    pico2d.clear_canvas()
    road.draw()
    for c in cars:
        c.draw()
    for c in coins:
        c.draw()
    for f in fires:
        f.draw()
    player.draw()
    info.draw()
    pico2d.update_canvas()
    pico2d.delay(DELAY)

def update():
    global road, player, cars, coins, fires, info
    road.update()   #도로 업데이트
    collision_check()       #충돌체크
    player.update()     #플레이어 차 업테이트
    for c in cars:
        c.update()          #상대 차들 업데이트
        if c.counter == 0:
            c.dir = random.randint(-1, 1)
    
    i, l = 0, len(fires)
    while i < l:         #폭발 업데이트
        if fires[i].frame <= Explosion.FRAME_SIZE:
            fires[i].update()
            i+=1
        else:
            del fires[i]    #프레임이 모두 출력되면 삭제하는 코드. update() 내부에서 스스로를 삭제할 수 있는 방법?
            l-=1
    
    i, l = 0, len(coins)    
    while i < l:         #코인 업데이트
        dx = (coins[i].x - info.coin.x)
        dy = (coins[i].y - info.coin.y)
        if dx*dx + dy*dy < 100:
            del coins[i]
            l-=1
        else:
            coins[i].update()
            i+=1
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
