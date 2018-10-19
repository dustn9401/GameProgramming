from pico2d import *
import game_framework
import random

class Road:
    def __init__(self):
        self.x = 400
        self.y = 300
        self.image = load_image('res/road.png')
        print(self.image)
    def draw(self):
        self.image.draw(self.x, self.y)
    def update(self):
        global mycar
        self.y -= mycar.speed
        if self.y > 500 or self.y < 100:
            self.y = 300

class Car:
    image = None
    def __init__(self, level):
        self.x = random.randint(200,600)
        self.y = random.randint(0,600)
        self.speed = random.uniform(1.0, 3.0)
        self.accel = 0
        self.dir = 0
        self.level = level
    def draw(self):
        self.image.clip_draw(0, 0, 30, 50, self.x, self.y)
    def update(self):
        global mycar
        self.x += 2 * self.dir
        self.y -= (mycar.speed - self.speed)        #내 차와의 상대속도만큼 y위치 변경
        self.speed += self.accel                    #속도 += 가속도
        if self.y < -100: self.y = 900
        if self.y > 900: self.y = -100

class Car_lev1(Car):
    def __init__(self):
        super().__init__(1)
        if Car_lev1.image == None:
            Car_lev1.image = pico2d.load_image('res/car_lev1.png')

class Car_lev2(Car):
    image = None
    def __init__(self):
        super().__init__(2)
        if Car_lev2.image == None:
            Car_lev2.image = pico2d.load_image('res/car_lev2.png')

def handle_events():
    global mycar, road
    events = get_events()
    for e in events:
        if e.type == SDL_QUIT:
            game_framework.quit()
        elif e.type == SDL_KEYDOWN:
            if e.key == SDLK_ESCAPE:
                game_framework.pop_state()
            elif e.key == SDLK_LEFT:
                mycar.dir -= 1
            elif e.key == SDLK_RIGHT:
                mycar.dir += 1
            elif e.key == SDLK_DOWN:
                mycar.accel -= 0.03
            elif e.key == SDLK_UP:
                mycar.accel += 0.03
        elif e.type == SDL_KEYUP:
            if e.key == SDLK_LEFT:
                mycar.dir += 1
            elif e.key == SDLK_RIGHT:
                mycar.dir -= 1
            elif e.key == SDLK_UP:
                mycar.accel -= 0.03
            elif e.key == SDLK_DOWN:
                mycar.accel += 0.03
                
def enter():
    global mycar, cars, road
    mycar = Car_lev1()
    mycar.x, mycar.y = 400,300
    cars = []
    for i in range(10):
        cars.append(Car_lev1())
        cars.append(Car_lev2())
    road = Road()

def exit():
    global road, mycar, cars
    del mycar, road, cars

def draw():
    global road, mycar, cars
    clear_canvas()
    road.draw()
    mycar.draw()
    for c in cars:
        c.draw()
    update_canvas()

def update():
    global road, mycar, cars
    road.update()
    mycar.update()
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
