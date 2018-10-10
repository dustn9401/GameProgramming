from pico2d import *
import game_framework
import random

class Road:
    def __init__(self):
        self.x = 400
        self.y = 400
        self.image = load_image('res/road.png')
        print(self.image)
    def draw(self):
        self.image.draw(self.x, self.y)

class Car:
    image = None
    def __init__(self):
        self.x = random.randint(0, 200)
        self.y = random.randint(90, 550)
        self.speed = random.uniform(1.0, 3.0)
        if Car.image == None:
            Car.image = load_image('res/car.png')
    def draw(self):
        Car.image.clip_draw(50, 50, 50, 50, self.x, self.y)

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
                car.x-=5
            elif e.key == SDLK_RIGHT:
                car.x+=5
            elif e.key == SDLK_DOWN:
                road.y-=car.speed
            elif e.key == SDLK_UP:
                road.y+=car.speed

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
    pass
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
