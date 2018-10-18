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
        global car
        self.y -= car.speed
        if self.y > 500 or self.y < 100:
            self.y = 300

class Car:
    image = None
    def __init__(self):
        self.x = 400
        self.y = 90
        self.speed = random.uniform(1.0, 3.0)
        self.accel = 0
        self.dir = 0
        if Car.image == None:
            Car.image = load_image('res/car.png')
    def draw(self):
        Car.image.clip_draw(0, 0, 30, 50, self.x, self.y)
    def update(self):
        self.x += 2 * self.dir
        self.speed += self.accel

def handle_events():
    global car, road
    events = get_events()
    for e in events:
        if e.type == SDL_QUIT:
            game_framework.quit()
        elif e.type == SDL_KEYDOWN:
            if e.key == SDLK_ESCAPE:
                game_framework.pop_state()
            elif e.key == SDLK_LEFT:
                car.dir -= 1
            elif e.key == SDLK_RIGHT:
                car.dir += 1
            elif e.key == SDLK_DOWN:
                car.accel -= 0.03
            elif e.key == SDLK_UP:
                car.accel += 0.03
        elif e.type == SDL_KEYUP:
            if e.key == SDLK_LEFT:
                car.dir += 1
            elif e.key == SDLK_RIGHT:
                car.dir -= 1
            elif e.key == SDLK_UP:
                car.accel -= 0.03
            elif e.key == SDLK_DOWN:
                car.accel += 0.03
                
def enter():
    global car, road
    car = Car()
    road = Road()

def exit():
    global road, car
    del car, road

def draw():
    global road, car
    clear_canvas()
    road.draw()
    car.draw()
    update_canvas()

def update():
    global road, car
    road.update()
    car.update()
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
