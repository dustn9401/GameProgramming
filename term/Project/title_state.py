from pico2d import *
import game_framework
import racing_state
class Title:
    def __init__(self):
        self.image = load_image('res/title.png')
        print(self.image)
    def draw(self):
        self.image.draw(400,300)

def handle_events():
    events = get_events()
    for e in events:
        if e.type == SDL_QUIT:
            game_framework.quit()
        elif e.type == SDL_KEYDOWN:
            if e.key == SDLK_ESCAPE:
                game_framework.quit()
            if e.key == SDLK_SPACE:
                game_framework.push_state(racing_state)

def enter():
    global title
    title = Title()

def exit():
    del title

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
    global title
    clear_canvas()
    title.draw()
    update_canvas()

def update():
    pass

# fill here


if __name__ == '__main__':
    main()


