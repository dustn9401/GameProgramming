import pico2d
import random
import math

class Grass:
    def __init__(self):
        self.x, self.y = 400, 30
        self.image = pico2d.load_image('grass.png')
    def draw(self):
        self.image.draw(self.x, self.y)
class Boy:
    def __init__(self):
        self.x, self.y = random.randint(100,500), random.randint(100,500)
        self.frame = random.randrange(0,8)
        self.image = pico2d.load_image('animation_sheet.png')
        self.speed = random.randrange(1,10)
    def update(self):
        self.frame = (self.frame + 1) % 8
        #self.x+=self.speed
    def draw(self):
        self.image.clip_draw(self.frame * 100, 100, 100, 100, self.x, 600 - self.y)
class Pointer:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.image = pico2d.load_image('hand_arrow.png')
        self.image.draw(self.x, self.y)
    def draw(self):
        self.image.draw(self.x, 600 - self.y)
def handle_events():
    global running, x,y, speed, mouse_x, mouse_y, waypoints
    events = pico2d.get_events()
    for event in events:
        if event.type == pico2d.SDL_QUIT:
            running = False
        elif event.type == pico2d.SDL_KEYDOWN:
            if event.key == pico2d.SDLK_ESCAPE:
                running = False
        elif event.type == pico2d.SDL_MOUSEMOTION:
            mouse_x,mouse_y = event.x, event.y
        elif event.type == pico2d.SDL_MOUSEBUTTONDOWN:
            if event.button == pico2d.SDL_BUTTON_LEFT:
                waypoints.append(Pointer(mouse_x, mouse_y))
            else:
                waypoints.clear()

def move(boy):
    global waypoints
    if mouse_x != boy.x or mouse_y != boy.y:
        if len(waypoints) == 0:
            x, y = mouse_x, mouse_y
        else:
            x, y = waypoints[0].x, waypoints[0].y

        dy = y - boy.y        #캐릭터를 원점으로 생각하여 현재 마우스 좌표에 대한 상대적인 위치 차이를 구함
        dx = x - boy.x
        if dx == 0:
            dx += 0.000001
        grad = dy / dx          #기울기
        if dx >= 0:         #마우스가 캐릭터보다 오른쪽에 있으면(1,4사분면)
            boy.x+=boy.speed * math.cos(math.atan(grad))
            boy.y+=boy.speed * math.sin(math.atan(grad))
        else:               #2,3 사분면의 경우
            boy.x-=boy.speed * math.cos(math.atan(grad))
            boy.y-=boy.speed * math.sin(math.atan(grad))

        if dx >= -1 and dx <= 1 and dy >= -1 and dy <= 1 and len(waypoints) > 0:
            del waypoints[0]
    


pico2d.open_canvas()
boys = [Boy() for i in range(20)]
waypoints = []
grass = Grass()
running = True
mouse_x, mouse_y = 0,0

while running:
    pico2d.clear_canvas()
    grass.draw()

    for b in boys:
        move(b)
        b.update()
        b.draw()
    for w in waypoints:
        w.draw()

    pico2d.update_canvas()
    handle_events()
    pico2d.delay(0.01)

pico2d.close_canvas()