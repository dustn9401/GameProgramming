import pico2d
import math
def handle_events():
    global running, x,y, speed, mouse_x, mouse_y
    events = pico2d.get_events()
    for event in events:
        if event.type == pico2d.SDL_QUIT:
            running = False
        elif event.type == pico2d.SDL_KEYDOWN:
            if event.key == pico2d.SDLK_ESCAPE:
                running = False
        elif event.type == pico2d.SDL_MOUSEMOTION:
            mouse_x,mouse_y = event.x, event.y
            
pico2d.open_canvas()
grass = pico2d.load_image('grass.png')
character = pico2d.load_image('animation_sheet.png')

running = True
x = 0
y = 0
mouse_x, mouse_y=0,0
frame = 0
speed = 5
while running:
    pico2d.clear_canvas()
    grass.draw(400, 30)

    if mouse_x != x or mouse_y != y:
        dy=mouse_y-y        #캐릭터를 원점으로 생각하여 현재 마우스 좌표에 대한 상대적인 위치 차이를 구함
        dx=mouse_x-x
        if dx == 0: dx = 0.000001
        grad=dy/dx          #기울기
        
        arctan=math.atan2(dy, dx)
        boy.x+=boy.speed * math.cos(arctan)
        boy.y+=boy.speed * math.sin(arctan)
            
    character.clip_draw(frame * 100, 100, 100, 100, x, 600-y)
    pico2d.update_canvas()
    handle_events()
    frame = (frame + 1) % 8

    pico2d.delay(0.01)

pico2d.close_canvas()
