import pico2d
import game_framework
import random
import math
import base
import background
import garage_state
import gameover_state
import time
import ui
import threading
#WIDTH, HEIGHT = pico2d.get_canvas_width(), pico2d.get_canvas_height() #window
#size
cw, ch = 800, 600
MAX_LEV = 9     #max level
MAX_INT_LENGTH = 10

LEFT, RIGHT, UP, STOP, DEAD = range(5)    #car state
NUM_CAR = None
NUM_TREE = 100
ROAD_L, ROAD_R = 100, 700
DELAY = 0.01      #draw 시 delay함수 호출, accel, dir 변수 함께 조정
mx, my = 0, 0

cars = None
player = None
info = None
wave_lev = 1
is_over = False
lock = False

def gameover():
    bgm.stop()

    global info, player
    player.gameover = True
    player.car.y_speed = 0
    player.car.x_speed = 0
    player.car.dir = 0
    garage_state.save_data()
    info.gameover_time = time.time()
    info.gameover_coin = player.coin
    gameover_state.earn_coin = info.gameover_coin - info.gamestart_coin
    gameover_state.live_time = info.gameover_time - info.gamestart_time

    time.sleep(2)
    game_framework.change_state(gameover_state)

# =============== 코인, 속도, 숫자 표시 관련 =====================
class Info(base.BaseObject):
    WIDTH, HEIGHT = 100, 100
    def __init__(self):
        self.x, self.y = 550, 550
        self.coin = Coin(self.x, self.y)
        self.btn = []
        self.lbl = []
        self.st = time.time()
        
        self.nano = 0
        self.counter_1ms = 0
        self.counter_10ms = 0
        self.counter_100ms = 0
        self.counter_s = 0
        self.counter_m = 0
        
        self.gamestart_time = time.time()
        self.gameover_time = 0
        self.gamestart_coin = player.coin
        self.gameover_coin = 0
        
        self.elapsed_total = 0
        self.elapsed = 0
        self.gameover_timer = 0

        self.current_game_time = 0
        self.waving = False
        self.temp_label_timer = 0
    def draw(self):
        ui.draw()
        self.coin.draw()
    def update(self):
        global player
        self.current_game_time = time.time() - self.gamestart_time
        self.ed = time.time()
        self.elapsed = self.ed - self.st
        self.st = self.ed

        self.lbl = [\
            ui.Label('가진 돈: %d $' % player.coin, self.x + 20, self.y, 30, ui.FONT_2),\
            ui.Label('속도: %.3f km/h' % player.car.y_speed*5, self.x + 20, self.y - 30, 30, ui.FONT_2),\
            ui.Label('얻은 돈: %d $' % (player.coin - self.gamestart_coin), self.x + 20, self.y - 60, 30, ui.FONT_2),\
            ui.Label('시간: %.3f 초' % self.current_game_time, self.x + 20, self.y - 90, 30, ui.FONT_2),\
            ]
        if self.waving:
            self.temp_label_timer = 5
            self.waving = False
        if self.temp_label_timer > 0:
            warning = ui.Label('교통량이 급증하고있습니다!!', 300, 500, 30, ui.FONT_3)
            warning.color = (255,0,0)
            self.lbl = [*self.lbl, warning]
            self.temp_label_timer -= self.elapsed
            
        ui.labels = self.lbl
        ui.buttons = self.btn
        ui.update()
        self.coin.update()
        self.coin.x, self.coin.y = self.x, self.y
        
        
        cnt = self.elapsed % 0.1
        self.counter_100ms+=cnt
        self.elapsed -= 0.1 * cnt
        cnt = self.elapsed % 0.01
        self.counter_10ms+=cnt
        self.elapsed -= 0.01 * cnt
        cnt = self.elapsed % 0.001
        self.counter_1ms+=cnt
        self.elapsed -= 0.001 * cnt
        self.nano += self.elapsed
        
        if self.nano > 0.001:
            self.counter_1ms += self.nano // 0.001
            self.nano %= 0.001
        
        if self.counter_1ms >= 10:  #10ms 마다 할일
            self.counter_10ms += self.counter_1ms // 10
            self.counter_1ms %= 10
            
        if self.counter_10ms >= 10:     #100ms 마다 할일
            self.counter_100ms += self.counter_10ms // 10
            self.counter_10ms %= 10                
                
        if self.counter_100ms >= 10:    #1s 마다 할일
            self.counter_s += self.counter_100ms // 10
            self.counter_100ms %= 10
            
        if self.counter_s >= 60:
            self.counter_s %= 60
            self.counter_m += 1
            
        if self.counter_s % 10 == 0:
            pass
            

        
#======================= 차 그리기 ======================
class Car(base.BaseObject):
    images = [None for i in range(MAX_LEV)]
    images_h = [None for i in range(MAX_LEV)]
    def __init__(self, level):
        self.x = random.randint(ROAD_L + 100, ROAD_R - 100)
        self.y = ch + 100
        self.accel = 0
        self.dir = 0
        self.level = level
        self.max_speed = garage_state.car_info[str(self.level)]['speed']
        self.y_speed = random.uniform(1.0, self.max_speed)
        self.x_speed = 200 * DELAY * math.log2(self.level + 1)
        self.state = STOP
        self.frame = 0
        self.max_frame = garage_state.car_info[str(self.level)]['frame']
        self.image = None
        if Car.images[self.level] == None:
            Car.images[self.level] = pico2d.load_image('res/img/lv_%d.png' % self.level)
            Car.images_h[self.level] = pico2d.load_image('res/img/lv_%d_h.png'%self.level)
            print('image: car lv%d' % self.level)
        self.image = Car.images[self.level]
        self.image_h = Car.images_h[self.level]
        self.WIDTH = self.image.w
        self.HEIGHT = self.image.h // self.max_frame
        self.st, self.ed = time.time(), 0

        self.hit = False    #맞았을때 효과이미지 출력용
        self.max_hp = garage_state.car_info[str(self.level)]['hp']
        self.hp = self.max_hp
    def draw(self):
        if self.hit:
            self.image_h.clip_draw(0, self.frame * (self.image.h // self.max_frame), self.image.w, self.image.h // self.max_frame, self.x, self.y)
            self.hit = False
        else:
            self.image.clip_draw(0, self.frame * (self.image.h // self.max_frame), self.image.w, self.image.h // self.max_frame, self.x, self.y)
        #self.image.clip_composite_draw(0,
        #self.frame*(self.image.h//self.max_frame), self.image.w,
        #self.image.h//self.max_frame, 0, 'r', self.x, self.y, 100, 100)
        self.drawRect()
    def update(self):
        global player, bg
        # ============= 좌표 업데이트 ==============
            
        self.x_speed = 200 * DELAY * self.dir * math.log2(self.level + 2)
        self.x = pico2d.clamp(100, self.x + self.x_speed, cw - 100)
        
        #self.y_speed = pico2d.clamp(-self.max_speed, self.y_speed + self.accel, self.max_speed)      #속도 += 가속도
        self.y_speed = pico2d.clamp(0, self.y_speed + self.accel, self.max_speed)      #속도 += 가속도
        self.y -= (player.car.y_speed - self.y_speed)

        # ============= 상태 업데이트 ==============
        if self.y_speed == 0:
            self.state = STOP
        elif self.dir == 1:
            self.state = RIGHT
        elif self.dir == -1:
            self.state = LEFT
        else:
            self.state = UP

        self.ed = time.time()
        if self.ed - self.st > 0.05:
            self.frame = (self.frame + 1) % self.max_frame
            self.st = self.ed
        
class Explosion(base.BaseObject):
    image = None
    WIDTH, HEIGHT = 128, 128
    FRAME_SIZE = 16
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.frame = 0
        if Explosion.image == None:
            Explosion.image = pico2d.load_image('res/img/Explosion.png')
            print('Explosion', Explosion.image)
        self.st, self.ed = time.time(), 0
        self.end = False
    def draw(self):
        Explosion.image.clip_draw((self.frame % 4) * Explosion.WIDTH, (self.frame // 4) * Explosion.HEIGHT, Explosion.WIDTH, Explosion.HEIGHT, self.x, self.y)
    def update(self):
        global player
        self.ed = time.time()
        if self.ed - self.st > 0.05: 
            self.frame += 1
            self.st = self.ed
        if self.frame > Explosion.FRAME_SIZE:
            self.end = True
class Death(base.BaseObject):
    images = [None for i in range(MAX_LEV)]
    def __init__(self, x, y, lev):
        self.x, self.y = x, y
        self.frame = 0
        self.level = lev
        self.max_frame = garage_state.car_info[str(self.level)]['death_frame']
        if Death.images[self.level] == None:
            Death.images[self.level] = pico2d.load_image('res/img/dead_lv%d.png' % self.level)
        self.image = Death.images[self.level]
        self.WIDTH, self.HEIGHT = self.image.w, self.image.h
        self.st, self.ed = time.time(), 0
        self.end = False
    def draw(self):
        if self.level == 0:
            self.image.clip_draw(0, (self.max_frame - self.frame - 1) * (self.image.h // self.max_frame), self.image.w, self.image.h // self.max_frame, self.x, self.y)
        else:
            self.image.clip_draw(self.frame * self.image.w // self.max_frame, 0, self.image.w // self.max_frame, self.image.h, self.x, self.y)
    def update(self):
        global player
        self.ed = time.time()
        if self.ed - self.st > 0.1: 
            self.frame += 1
            self.st = self.ed
        if self.frame > self.max_frame:
            self.end = True
class Coin(base.BaseObject):
    image = None
    WIDTH, HEIGHT = 50, 50
    FRAME_SIZE = 10
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.frame = 0
        self.speed = 10
        self.end = False
        if Coin.image == None:
            Coin.image = pico2d.load_image('res/img/coin.png')
            print('Coin', self.image)
        self.st, self.ed = time.time(), 0
    def draw(self):
        Coin.image.clip_draw(self.frame * self.WIDTH, 0, self.WIDTH, self.HEIGHT, self.x, self.y)
        #self.image.clip_composite_draw(self.frame*100, 300, 100, 100,
        #math.pi/2, '', self.x, self.y, 100, 100)
    def update(self):
        global info
        self.ed = time.time()
        if self.ed - self.st > 0.05:
            self.frame = (self.frame + 1) % self.FRAME_SIZE
            self.st = self.ed
        dx, dy = info.coin.x - self.x, info.coin.y - self.y
        arctan = math.atan2(dy, dx)
        self.x += self.speed * math.cos(arctan)
        self.y += self.speed * math.sin(arctan)
        dx = (self.x - info.coin.x)
        dy = (self.y - info.coin.y)
        if dx * dx + dy * dy < 100:
            self.end = True
            
class Bullet(base.BaseObject):
    image = None
    def __init__(self, x, y, angle):
        if Bullet.image == None:
            Bullet.image = pico2d.load_image('res/img/bullet.png')
        self.WIDTH = Bullet.image.w
        self.HEIGHT = Bullet.image.h
        self.x = x
        self.y = y
        self.speed = 20
        self.xspeed = self.speed * math.cos(angle)
        self.yspeed = self.speed * math.sin(angle)
    def draw(self):
        Bullet.image.draw(self.x, self.y)
        #self.drawRect()
    def update(self):
        self.x += self.xspeed
        self.y += self.yspeed

class Player(base.BaseObject):
    endl = False
    def __init__(self):
        garage = garage_state.garage
        self.coin = garage_state.player_info['coin']
        self.level = garage.slot[garage.select]
        self.car = Car(self.level)
        self.car.x = cw // 2
        self.car.y = cw // 4
        self.car.y_speed = 0
        self.st, self.ed = time.time(), 0
        self.shoot = False
        self.shoot_speed = garage_state.car_info[str(self.car.level)]['shoot_speed']
        self.shoot_timer = 0
        self.bullets = []

        self.gameover = False

    def draw(self):
        self.car.draw()
        for b in self.bullets:
            b.draw()
    def update(self):
        global bg, cars, info
        garage_state.player_info['coin'] = self.coin
        
        self.st = self.ed        

        if not self.gameover:
            self.car.update()

        # ============ 총알발사 ============
            self.shoot_timer += info.elapsed
            if self.shoot and self.shoot_timer > self.shoot_speed:
                dx = mx - self.car.x
                dy = my - self.car.y
                arctan = math.atan2(dy, dx)
                self.bullets.append(Bullet(self.car.x, self.car.y, arctan))

                if self.car.level >= 2:
                    self.bullets.append(Bullet(self.car.x, self.car.y, arctan + 0.2))
                    self.bullets.append(Bullet(self.car.x, self.car.y, arctan - 0.2))
                if self.car.level >= 4:
                    self.bullets.append(Bullet(self.car.x, self.car.y, arctan + 0.4))
                    self.bullets.append(Bullet(self.car.x, self.car.y, arctan - 0.4))
                if self.car.level >= 6:
                    self.bullets.append(Bullet(self.car.x, self.car.y, arctan + 0.6))
                    self.bullets.append(Bullet(self.car.x, self.car.y, arctan - 0.6))
                if self.car.level >= 8:
                    self.bullets.append(Bullet(self.car.x, self.car.y, arctan + 0.8))
                    self.bullets.append(Bullet(self.car.x, self.car.y, arctan - 0.8))
                self.shoot_timer = 0
        else:
            self.car.x = self.car.y = -100
            self.car.y_speed = self.car.x_speed = 0
            self.car.dir = 0

        # =========== 총알제거 ===============
        for i, b in enumerate(self.bullets):
            b.update()
            if b.x > cw or b.x < 0 or b.y > ch or b.y < 0:
                del self.bullets[i]

def handle_events():
    global road, player, mx, my
    events = pico2d.get_events()
    for e in events:
        if e.type == pico2d.SDL_QUIT:
            garage_state.save_data()
            game_framework.quit()
        elif e.type == pico2d.SDL_KEYDOWN and not player.gameover:
            if e.key == pico2d.SDLK_ESCAPE:
                garage_state.save_data()
                game_framework.change_state(garage_state)
            if e.key == pico2d.SDLK_a:
                player.car.dir -= 1
            elif e.key == pico2d.SDLK_d:
                player.car.dir += 1
            elif e.key == pico2d.SDLK_s:
                pass
                player.car.accel -= DELAY * 10 * math.log2(player.car.level + 2)
#                player.car.y_speed = -player.car.max_speed
            elif e.key == pico2d.SDLK_w:
                player.car.accel += DELAY * 10 * math.log2(player.car.level + 2)
#                player.car.y_speed = player.car.max_speed
        elif e.type == pico2d.SDL_KEYUP and not player.gameover:
            if e.key == pico2d.SDLK_a:
                player.car.dir += 1
            elif e.key == pico2d.SDLK_d:
                player.car.dir -= 1
            elif e.key == pico2d.SDLK_w:
                player.car.accel -= DELAY * 10 * math.log2(player.car.level + 2)
#                player.car.y_speed = 0
            elif e.key == pico2d.SDLK_s:
                player.car.accel += DELAY * 10 * math.log2(player.car.level + 2)
#                player.car.y_speed = 0
        elif e.type == pico2d.SDL_MOUSEMOTION:
            mx, my = e.x, ch - e.y
        elif e.type == pico2d.SDL_MOUSEBUTTONDOWN:
            if e.button == pico2d.SDL_BUTTON_LEFT and not player.gameover:
                player.shoot = True
        elif e.type == pico2d.SDL_MOUSEBUTTONUP:
            if e.button == pico2d.SDL_BUTTON_LEFT and not player.gameover:
                player.shoot = False

def draw_death(car):
    global fires
    if car.level < 5 or car.level == 7:
        fires.append(Death(car.x, car.y, car.level))
    else:
        fires.append(Explosion(car.x, car.y))
        
def checkRect(r1, r2):
    if r1[0][0] > r2[1][0] or r1[0][1] > r2[1][1] or r1[1][0] < r2[0][0] or r1[1][1] < r2[0][1]:
        return False
    return True
def collision_check():
    global coins, fires, end_time, earn_coin, is_over, player, cars, bullets, lock
    while not is_over:
        
        pRect = player.car.getRect()
        lock = True
        for idx, c in enumerate(cars):
        
            # ============ 플레이어와 적 차량 충돌체크 ==============
            if checkRect(pRect, c.getRect()):
                if player.car.level > c.level:
                    get = (c.level + 1) * 2
                    draw_death(c)
                    del cars[idx]
                    for i in range(get):    #터트린 차량의 레벨에 비례한 코인 생성
                        coins.append(Coin(c.x + random.randint(-20, 20), c.y + random.randint(-20, 20))) 
                    player.coin += get
                    get_coin_bgm.play()
                else:
                    is_over = True
                    gameover_bgm.play()
                    draw_death(player.car)
        
            # =========== 총알과 적 차량 충돌체크 ============
            for i, b in enumerate(player.bullets):
                bRect = b.getRect()
                if checkRect(bRect, c.getRect()):
                    del player.bullets[i]
                    if c.hp <= 1:
                        get = (c.level + 1) * 2
                        draw_death(c)
                        del cars[idx]
                        for i in range(get):    #터트린 차량의 레벨에 비례한 코인 생성
                            coins.append(Coin(c.x + random.randint(-40, 40), c.y + random.randint(-40, 40))) 
                        player.coin += get
                        get_coin_bgm.play()
                    else:
                        c.hp -= 1
                        c.hit = True
        lock = False
        pico2d.delay(DELAY*2)

def wave(level):
    global cars
    print('wave level: ', level)
    wave_cars = [Car(pico2d.clamp(player.car.level, player.car.level + 3, MAX_LEV - 1)) for _ in range(level*10)]
    w = (cw-200)/len(wave_cars)
    wave_cars[0].y = ch
    wave_cars[0].x = 0
    for i in range(1, len(wave_cars)):
        wave_cars[i].x = wave_cars[i-1].x + w
        wave_cars[i].y_speed = 5
        wave_cars[i].y = ch + 50
    cars += wave_cars
def enter():
    global player, cars, coins, info, fires, player_data, bg, start_time, wav_lev, collision_check_thread, is_over
    player = Player()

    fires = []
    info = Info()
    coins = []
    cars = []

    lev = player.car.level

    global NUM_CAR
    NUM_CAR = (garage_state.garage.difficulty + 1) * 20
    for i in range(NUM_CAR):
        #내 차보다 최대 2레벨 높은것만 나오도록
        cars.append(Car(random.randrange(0, lev+3 if lev+3 < MAX_LEV else MAX_LEV)))
    bg = background.Background()

    global bgm, gameover_bgm, get_coin_bgm
    bgm = pico2d.load_music('res/sound/bgm.mp3')
    gameover_bgm = pico2d.load_wav('res/sound/dead.wav')
    get_coin_bgm = pico2d.load_wav('res/sound/coin.wav')
    bgm.set_volume(64)
    gameover_bgm.set_volume(64)
    get_coin_bgm.set_volume(64)
    bgm.repeat_play()

    wav_lev = 1
    is_over = False
    collision_check_thread = threading.Thread(target = collision_check)
    collision_check_thread.start()

def exit():
    global bg, player, cars, coins, fires, info, bgm, gameover_bgm, get_coin_bgm
    del player, bg, cars, coins, fires, info, bgm, gameover_bgm, get_coin_bgm

def draw():
    global bg, player, cars, coins, fires
    pico2d.clear_canvas()
    bg.draw()
    for c in cars:
        c.draw()
    for c in coins:
        c.draw()
    for f in fires:
        f.draw()
    player.draw()
    for c in bg.clouds:
        c.draw()
    info.draw()
    pico2d.update_canvas()

cur, bef = 0, 0
def update():
    global bg, player, cars, coins, fires, info, wave_lev
    global cur, bef, is_over


    bg.update()   #도로 업데이트

    for i, c in enumerate(cars):
        c.update()          #상대 차들 업데이트
        if random.randint(0, 100) == 0:
            c.dir = random.randint(-1, 1)
        if c.y < -100 or c.y > ch + 200 and not lock:
            lock = True
            if len(cars) > NUM_CAR:
                del cars[i]
            if len(cars) < NUM_CAR:
                cars.append(Car(random.randrange(0, player.car.level+3 if player.car.level+3 < MAX_LEV else MAX_LEV)))
            lock = False
            
    for i,f in enumerate(fires):
        f.update()
        if f.end: del fires[i]
    for i,c in enumerate(coins):
        c.update()
        if c.end: del coins[i]

    info.update()
    player.update()

    cur = int(info.current_game_time)
    if cur > 10 and cur % 20 == 15:
        info.waving = True
    if cur > 10 and cur % 20 == 0:
        if cur != bef:
            bef = cur
            wave(wave_lev)
            wave_lev += 1

    if is_over:   #1초후 종료
        info.gameover_timer += info.elapsed
        if info.gameover_timer > 1:
            gameover()
    #else:
    #    collision_check()
    pico2d.delay(DELAY)


def pause():
    pass
def resume():
    pass

def main():
    pico2d.open_canvas()
    running = True
    enter()
    while running:
        handle_events()
        update()
        draw()
    exit()
    pico2d.close_canvas()

if __name__ == '__main__':
    main()
