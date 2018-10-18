from pico2d import *
import game_framework
import garage_state
class Title:
    def __init__(self):
        self.image = load_image('res/title.png')
        print(self.image)
    def draw(self):
        self.image.draw(400,300)
class ButtonStart:
    def __init__(self):
        self.image = load_image('res/gamestart.png')
        print(self.image)
    def draw(self):
        self.image.draw(400,200)
def handle_events():
    events = get_events()
    for e in events:
        if e.type == SDL_QUIT:
            game_framework.quit()
        elif e.type == SDL_KEYDOWN:
            if e.key == SDLK_ESCAPE:
                game_framework.quit()
            if e.key == SDLK_SPACE:
                game_framework.push_state(garage_state)
        elif e.type == SDL_MOUSEBUTTONDOWN:
            if e.button == SDL_BUTTON_LEFT:
                if e.x > 342 and e.x < 491 and e.y > 430 and e.y < 494:
                    game_framework.push_state(garage_state)
                print('%d, %d'%(e.x, e.y))

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
    clear_canvas()
    title.draw()
    start.draw()
    update_canvas()

def update():
    pass

# fill here


if __name__ == '__main__':
    main()


