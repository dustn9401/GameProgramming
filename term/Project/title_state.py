import pico2d
import game_framework
import garage_state
import base
class Title:
    def __init__(self):
        self.image = pico2d.load_image('res/title.png')
        print('Title', self.image)
    def draw(self):
        self.image.draw(400,300)
class ButtonStart(base.BaseObject):
    image = None
    WIDTH, HEIGHT = 330, 140
    def __init__(self):
        self.x, self.y = 400, 100
        if ButtonStart.image == None:
            ButtonStart.image = pico2d.load_image('res/gamestart.png')
        print('ButtonStart', self.image)
    def draw(self):
        self.image.draw(self.x, self.y)
        self.drawRect()
    def update(self):
        pass
def handle_events():
    global start
    events = pico2d.get_events()
    for e in events:
        if e.type == pico2d.SDL_QUIT:
            game_framework.quit()
        elif e.type == pico2d.SDL_KEYDOWN:
            if e.key == pico2d.SDLK_ESCAPE:
                game_framework.quit()
            if e.key == pico2d.SDLK_SPACE:
                game_framework.push_state(garage_state)
        elif e.type == pico2d.SDL_MOUSEBUTTONDOWN:
            if e.button == pico2d.SDL_BUTTON_LEFT:
                if start.inRect(e.x, 600 - e.y):
                    game_framework.push_state(garage_state)

def enter():
    global title, start
    title = Title()
    start = ButtonStart()

def exit():
    global title, start
    del title, start

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
    global title, start
    pico2d.clear_canvas()
    title.draw()
    start.draw()
    pico2d.update_canvas()

def update():
    pass

# fill here


if __name__ == '__main__':
    main()


