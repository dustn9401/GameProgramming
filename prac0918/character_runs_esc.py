import pico2d

def handle_events():
    global running, x,y, speed,dir, mouse_x, mouse_y
    events = pico2d.get_events()
    for event in events:
        if event.type == pico2d.SDL_QUIT:
            running = False
        elif event.type == pico2d.SDL_KEYDOWN:
            if event.key == pico2d.SDLK_ESCAPE:
                running = False
            elif event.key == pico2d.SDLK_RIGHT:
                dir+=1
            elif event.key == pico2d.SDLK_LEFT:
                dir-=1
        elif event.type == pico2d.SDL_KEYUP:
            if event.key == pico2d.SDLK_RIGHT:
                dir-=1
            elif event.key == pico2d.SDLK_LEFT:
                dir+=1
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
dir = 0
while running:
    pico2d.clear_canvas()
    grass.draw(400, 30)

    if mouse_x != x and mouse_y != y:
        dy=mouse_y-y
        dx=mouse_x-x
        grad=dy/dx
        x+=speed*(grad)
        y+=speed*(1/grad)
    character.clip_draw(frame * 100, 100, 100, 100, x, 600-y)
    pico2d.update_canvas()
    handle_events()
    frame = (frame + 1) % 8
    x+=dir * 5

    pico2d.delay(0.01)

pico2d.close_canvas()
