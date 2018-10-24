import game_framework
import racing_state
import logo_state
import pico2d

pico2d.open_canvas(200,200)
img = pico2d.load_image('res/coin.png')
img.clip_draw(0, 0, 30, 50, 100, 100)
