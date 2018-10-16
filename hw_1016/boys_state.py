from pico2d import *
import game_framework
import random
import json
#data = {
#    'boy1': {'x':100, 'y':100, 'speed':1, 'frame':0, 'state':0},
#    'boy2': {'x':50, 'y':100, 'speed':1, 'frame':1, 'state':0},
#    'boy3': {'x':200, 'y':160, 'speed':1, 'frame':2, 'state':0},
#    'boy4': {'x':300, 'y':330, 'speed':1, 'frame':3, 'state':0},
#    'boy5': {'x':400, 'y':440, 'speed':1, 'frame':5, 'state':0},
#    'boy6': {'x':500, 'y':20, 'speed':1, 'frame':4, 'state':0},
#    'boy7': {'x':600, 'y':250, 'speed':1, 'frame':6, 'state':0},
#    'boy8': {'x':400, 'y':550, 'speed':1, 'frame':5, 'state':0},
#    'boy9': {'x':450, 'y':450, 'speed':1, 'frame':2, 'state':0},
#    'boy10': {'x':650, 'y':100, 'speed':1, 'frame':1, 'state':0},
#    }
#data_str = json.dumps(data)
#f = open("../res/team_data.txt", 'w')
#f.write(data_str)
#f.close()
#print(data_str)



BOYS_NUM=10
class Grass:
    def __init__(self):
        self.image = load_image('../res/grass.png')
        print(self.image)
    def draw(self):
        self.image.draw(400, 30)

class Boy:
    image = None
    def __init__(self):
        print("Creating..")
        self.x = random.randint(0, 200)
        self.y = random.randint(90, 550)
        self.speed = random.uniform(1.0, 3.0)
        self.frame = random.randint(0, 7)
        self.waypoints = []
        self.state = random.randint(2,3)
        if Boy.image == None:
            Boy.image = load_image('../res/animation_sheet.png')
            Boy.wp = load_image('../res/hand_arrow.png')
    def draw(self):
        for wp in self.waypoints:
            Boy.wp.draw(wp[0], wp[1])
        Boy.image.clip_draw(self.frame * 100, self.state * 100, 100, 100, self.x, self.y)
    def update(self):
        self.frame = (self.frame + 1) % 8
        if len(self.waypoints) > 0:
            tx, ty = self.waypoints[0]
            dx, dy = tx - self.x, ty - self.y
            self.state = 0 if dx < 0 else 1
            dist = math.sqrt(dx ** 2 + dy ** 2)
            if dist > 0:
                self.x += self.speed * dx / dist
                self.y += self.speed * dy / dist

                if dx < 0 and self.x < tx: self.x = tx
                if dx > 0 and self.x > tx: self.x = tx
                if dy < 0 and self.y < ty: self.y = ty
                if dy > 0 and self.y > ty: self.y = ty

                if (tx, ty) == (self.x, self.y):
                    del self.waypoints[0]
        else:
            if self.state == 0: self.state = 2
            if self.state == 1: self.state = 3

span = 50
def handle_events():
    global boys
    global span
    events = get_events()
    for e in events:
        if e.type == SDL_QUIT:
            game_framework.quit()
        elif e.type == SDL_KEYDOWN:
            if e.key == SDLK_ESCAPE:
                game_framework.pop_state()
            elif e.key in range(SDLK_1, SDLK_9 + 1):
                span = 20 * (e.key - SDLK_0)

        elif e.type == SDL_MOUSEBUTTONDOWN:
            if e.button == SDL_BUTTON_LEFT:
                tx, ty = e.x, 600 - e.y
                for b in boys:
                    bx = tx + random.randint(-span, span)
                    by = ty + random.randint(-span, span)
                    b.waypoints += [ (bx, by) ]
            else:
                for b in boys:
                    b.waypoints = []

def enter():
    global boys, grass
    #open_canvas()
    boys = []

    team_data_file = open('../res/boys_data.json', 'r')
    team_data = json.load(team_data_file)
    team_data_file.close()

    for e in team_data['boys']:
        b = Boy()
        b.name = e['name']
        b.x, b.y = e['x'], e['y']
        b.speed = e['speed']
        boys.append(b)

    grass = Grass()

def exit():
    global boys, grass
    del boys, grass

# def main():
#     global running
#     enter()
#     while running:
#         handle_events()
#         print(running)
#         update()
#         draw()
#     exit()

def draw():
    global grass, boys
    clear_canvas()
    grass.draw()
    for b in boys:
        b.draw()
    update_canvas()

def update():
    global boys
    for b in boys:
        b.update()
    delay(0.01)

# fill here
def pause():
    pass
def resume():
    pass

if __name__ == '__main__':
    main()
