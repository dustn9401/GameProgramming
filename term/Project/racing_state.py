import pico2d
import game_framework
import random
WIDTH, HEIGHT = 800, 600
MAX_LEV = 3
LEFT, RIGHT, UP, STOP = range(4)
class Road:
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

class Car:
    image = [[] for i in range(MAX_LEV)]
    def __init__(self, level):
        self.x = random.randint(0 + 200, WIDTH - 200)
        self.y = random.randint(0, HEIGHT)
        self.speed = random.uniform(1.0, 3.0)
        self.accel = 0
        self.dir = 0
        self.level = level
        self.state = STOP
        if len(Car.image[self.level]) == 0:
            Car.image[self.level].append(pico2d.load_image('res/car_lev%d_l.png'%(self.level)))
            Car.image[self.level].append(pico2d.load_image('res/car_lev%d_r.png'%(self.level)))
            Car.image[self.level].append(pico2d.load_image('res/car_lev%d_u.png'%(self.level)))
            Car.image[self.level].append(pico2d.load_image('res/car_lev%d_s.png'%(self.level)))
    def draw(self):
        self.image[self.level][self.state].draw(self.x, self.y)
    def update(self):
        global player
        self.x = pico2d.clamp(0 + 100, self.x + (self.dir/2), WIDTH - 100)     #x좌표 최소100, 최대700
        self.y -= (player.car.speed - self.speed)        #내 차와의 상대속도만큼 y위치 변경
        self.speed += self.accel                    #속도 += 가속도
        if self.y < -100: self.y = 900
        if self.y > 900: self.y = -100

        # ============= 차량 움직임 상태 ==============

        if self.speed == 0:
            self.state = STOP
        elif self.dir == 1:
            self.state = RIGHT
        elif self.dir == -1:
            self.state = LEFT
        else:
            self.state = UP

class Player:
    def __init__(self, level):
        self.coin = 0
        self.car = Car(level)

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
                player.car.accel -= 0.01
            elif e.key == pico2d.SDLK_UP:
                player.car.accel += 0.01
        elif e.type == pico2d.SDL_KEYUP:
            if e.key == pico2d.SDLK_LEFT:
                player.car.dir += 1
            elif e.key == pico2d.SDLK_RIGHT:
                player.car.dir -= 1
            elif e.key == pico2d.SDLK_UP:
                player.car.accel -= 0.01
            elif e.key == pico2d.SDLK_DOWN:
                player.car.accel += 0.01
                
def collision_check():
    global player, cars

def enter():
    global player, cars, road
    player = Player(1)
    player.car.x, player.car.y = 400,200
    cars = []
    for i in range(10):
        cars.append(Car(random.randrange(1,2)))
    road = Road()

def exit():
    global road, player, cars
    del player, road, cars

def draw():
    global road, player, cars
    pico2d.clear_canvas()
    road.draw()
    player.car.draw()
    for c in cars:
        c.draw()
    pico2d.update_canvas()

def update():
    global road, player, cars
    road.update()
    player.car.update()
    for c in cars:
        c.update()
def pause():
    pass
def resume():
    pass

def main():
    global running
    enter()
    while running:
        handle_events()
        print(running)
        update()
        draw()
    exit()

if __name__ == '__main__':
    main()
