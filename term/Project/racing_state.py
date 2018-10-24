import pico2d
import game_framework
import random
import math
WIDTH, HEIGHT = 800, 600    #window size
MAX_LEV = 6     #max level
MAX_SPEEDS = [i*10 for i in range(MAX_LEV)]

LEFT, RIGHT, UP, STOP, DEAD = range(5)    #car state
LOAD_W,LOAD_H = 800, 1534
COIN_W, COIN_H = 50, 50
COIN_FRAME_SIZE = 10
CAR_W, CAR_H = 45, 62
EXPLOSION_W, EXPLOSION_H = 128, 128
EXPLOSION_FRAME_SIZE = 16
NUM_CAR = 20
NUM_TREE = 100

class BaseObject:
    def __init__(self):
        print('do not create')
    def draw(self):
        raise NotImplementedError()
    def update(self):
        raise NotImplementedError()
class Tree(BaseObject):
    image = None
    def __init__(self):
        self.x = random.randint(0,180) if random.randint(0,1) else random.randint(WIDTH-180, WIDTH)
        self.y = random.randint(0, HEIGHT)
        if Tree.image == None:
            Tree.image = pico2d.load_image('res/tree.png')
            print(self.image)
    def draw(self):
        Tree.image.draw(self.x, self.y)
    def update(self):
        global player
        self.y -= player.car.speed
        if self.y < 0: self.y = HEIGHT+200
class Road(BaseObject):
    def __init__(self):
        self.x = WIDTH//2
        self.y = HEIGHT//2
        self.image = pico2d.load_image('res/road.png')
        print(self.image)
    def draw(self):
        self.image.draw(self.x, self.y)
    def update(self):
        global player
        self.y -= player.car.speed
        if self.y > 500 or self.y < 100:
            self.y = 300

class Car(BaseObject):
    image = None
    def __init__(self, level):
        self.x = random.randint(0 + 200, WIDTH - 200)
        self.y = random.randint(0, HEIGHT)
        self.accel = 0
        self.dir = 0
        self.level = level
        self.speed = random.uniform(1.0, MAX_SPEEDS[self.level])
        self.state = STOP
        if Car.image == None:
            Car.image = pico2d.load_image('res/car.png')
    def draw(self):
        Car.image.clip_draw(self.state*CAR_W, (self.level-1)*CAR_H, CAR_W, CAR_H, self.x, self.y)
        
        rt = getRect(self)
        pico2d.draw_rectangle(rt[0][0], rt[0][1], rt[1][0], rt[1][1])
        #clip_composite_draw(self.frame*100, 300, 100, 100, math.pi/2, '', self.x, self.y, 100, 100)
    def update(self):
        global player
        if self.state == DEAD:
            self.reset()
        # ============= 좌표 업데이트 ==============
        self.x = pico2d.clamp(0 + 100, self.x + 2*self.dir, WIDTH - 100)     #x좌표 최소100, 최대700
        self.y -= (player.car.speed - self.speed)        #내 차와의 상대속도만큼 y위치 변경
        self.speed = pico2d.clamp(-MAX_SPEEDS[self.level], self.speed + self.accel, MAX_SPEEDS[self.level])      #속도 += 가속도
        if self.y < -100 or self.y > 900:
            self.reset()

        # ============= 상태 업데이트 ==============
        if self.speed == 0:
            self.state = STOP
        elif self.dir == 1:
            self.state = RIGHT
        elif self.dir == -1:
            self.state = LEFT
        else:
            self.state = UP
    def reset(self):
        self. x = random.randint(200, WIDTH - 200)
        self. y = 0-100 if random.randint(0,1) else HEIGHT+100
        self.speed = random.uniform(1.0, MAX_SPEEDS[self.level])
class Explosion(BaseObject):
    image = None
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.frame = 0
        if Explosion.image == None:
            Explosion.image = pico2d.load_image('res/Explosion.png')
            print(self.image)
    def draw(self):
        Explosion.image.clip_draw((self.frame%4)*EXPLOSION_W, (self.frame//4)*EXPLOSION_H, EXPLOSION_W, EXPLOSION_H, self.x, self.y)
    def update(self):
        global player
        self.y -= player.car.speed
        self.frame += 1
        
class Coin(BaseObject):
    image = None
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.frame = 0
        self.speed = 10
        if Coin.image == None:
            Coin.image = pico2d.load_image('res/coin.png')
            print(self.image)
    def draw(self):
        Coin.image.clip_draw(self.frame*COIN_W, 0, COIN_W, COIN_H, self.x, self.y)
        #self.image.clip_composite_draw(self.frame*100, 300, 100, 100, math.pi/2, '', self.x, self.y, 100, 100)
    def update(self):
        global info
        self.frame = (self.frame + 1) % 10
        dx, dy = info.coin.x - self.x, info.coin.y - self.y
        arctan = math.atan2(dy, dx)
        self.x += self.speed*math.cos(arctan)
        self.y += self.speed*math.sin(arctan)
class Player:
    def __init__(self, level):
        self.coin = 0
        self.car = Car(level)
class Info(BaseObject):
    def __init__(self):
        self.x, self.y = 700, 500
        self.coin = Coin(self.x, self.y)
    def draw(self):
        self.coin.draw()
    def update(self):
        self.coin.update()
        self.coin.x, self.coin.y = self.x, self.y
    
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
                player.car.accel -= 0.1
            elif e.key == pico2d.SDLK_UP:
                player.car.accel += 0.1
        elif e.type == pico2d.SDL_KEYUP:
            if e.key == pico2d.SDLK_LEFT:
                player.car.dir += 1
            elif e.key == pico2d.SDLK_RIGHT:
                player.car.dir -= 1
            elif e.key == pico2d.SDLK_UP:
                player.car.accel -= 0.1
            elif e.key == pico2d.SDLK_DOWN:
                player.car.accel += 0.1

def getRect(car):
    return [[car.x - CAR_W//2, car.y - CAR_H//2], [car.x + CAR_W//2, car.y + CAR_H//2]]
def checkRect(r1, r2):
    if r1[0][0] > r2[1][0] or r1[0][1] > r2[1][1] or r1[1][0] < r2[0][0] or r1[1][1] < r2[0][1]:
        return False
    return True
def collision_check():
    global player, cars, coins, fires
    pRect = getRect(player.car)
    for c in cars:
        if checkRect(pRect, getRect(c)):
            c.state = DEAD
            fires.append(Explosion(c.x, c.y))
            coins.append(Coin(c.x, c.y))
            
            
def enter():
    global player, cars, road, coins, info, fires, trees
    fires = []
    info = Info()
    coins = []
    player = Player(1)
    player.car.x, player.car.y = 400,200
    cars = []
    trees = []
    for i in range(NUM_CAR):
        cars.append(Car(random.randrange(1,MAX_LEV)))
    for i in range(NUM_TREE):
        trees.append(Tree())
    road = Road()

def exit():
    global road, player, cars, coins, fires, trees
    del player, road, cars, coins, fires, trees

def draw():
    global road, player, cars, coins, fires
    pico2d.clear_canvas()
    road.draw()
    for t in trees:
        t.draw()
    for c in cars:
        c.draw()
    for c in coins:
        c.draw()
    for f in fires:
        f.draw()
    player.car.draw()
    info.draw()
    pico2d.update_canvas()
    pico2d.delay(0.01)

def update():
    global road, player, cars, coins, fires, info
    road.update()   #도로 업데이트
    collision_check()       #충돌체크
    player.car.update()     #플레이어 차 업테이트
    for c in cars:
        c.update()          #상대 차들 업데이트
    
    i, l = 0, len(fires)
    while i < l:         #폭발 업데이트
        if fires[i].frame <= EXPLOSION_FRAME_SIZE:
            fires[i].update()
            i+=1
        else:
            del fires[i]
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

    for t in trees:
        t.update()
    info.update()
    #pico2d.delay(0.01)
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
