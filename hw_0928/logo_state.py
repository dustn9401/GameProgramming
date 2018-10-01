from pico2d import *
import game_framework
import title_state

class Credit:
    def __init__(self):
        self.image = load_image('../res/kpu_credit.png')
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

def enter():
    global credit
    open_canvas()

    credit = Credit()

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
    global credit
    clear_canvas()
    credit.draw()
    update_canvas()
    delay(1)
    game_framework.run(title_state)     #logo state는 스택에 넣지 않고 타이틀 바로 실행

def update():
    pass

# fill here

def exit():
    close_canvas()

if __name__ == '__main__':
    main()


