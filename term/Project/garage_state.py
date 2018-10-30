import pico2d
import game_framework
import racing_state

class Garage:
    def __init__(self):
        self.image = pico2d.load_image('res/garage.png')
        print('Garage', self.image)
    def draw(self):
        self.image.draw(400,300)


def handle_events():
    events = pico2d.get_events()
    for e in events:
        if e.type == pico2d.SDL_QUIT:
            game_framework.quit()
        elif e.type == pico2d.SDL_KEYDOWN:
            if e.key == pico2d.SDLK_ESCAPE:
                game_framework.pop_state()
            if e.key == pico2d.SDLK_SPACE:
                game_framework.push_state(racing_state)
        elif e.type == pico2d.SDL_MOUSEBUTTONDOWN:
            if e.button == pico2d.SDL_BUTTON_LEFT:
                if e.x > 442 and e.x < 741 and e.y > 503 and e.y < 587:
                    game_framework.push_state(racing_state)
                    
def enter():
    global garage
    garage = Garage()

def exit():
    global garage
    del garage

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

def draw():
    global garage
    pico2d.clear_canvas()
    garage.draw()
    pico2d.update_canvas()

def update():
    pass

# fill here

if __name__ == '__main__':
    main()


