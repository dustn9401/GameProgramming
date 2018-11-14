import racing_state
import pico2d
import random
cw = 800
ch = 600
TREE = 100
CLOUD = 20
class Background:
    def __init__(self):
        self.image = pico2d.load_image('res/road.png')
        print('Road', self.image)
        self.width = self.image.w
        self.height = self.image.h
        self.lx = cw/2
        self.rx = self.lx + self.width
        self.dy = ch/2
        self.uy = self.dy + self.height
        self.trees = [Tree() for i in range(TREE)]
        self.clouds = [Cloud() for i in range(CLOUD)]
    def draw(self):
        self.image.draw(self.lx, self.dy)
        self.image.draw(self.lx, self.uy)
        self.image.draw(self.rx, self.dy)
        self.image.draw(self.rx, self.uy)
        for t in self.trees: t.draw()
        for c in self.clouds: c.draw()
    def update(self):
        player = racing_state.player
        self.dy -= player.car.y_speed
        if self.dy < -ch/2: 
            self.dy = ch/2
        if self.dy > ch/2: 
            self.dy = -ch/2
        self.uy = self.dy + self.height
                
        self.lx -= player.car.x_speed
        if self.lx < -cw/2: 
            self.lx = cw/2
        if self.lx > cw/2: 
            self.lx = -cw/2
        self.rx = self.lx + self.width
        
        for t in self.trees:
            t.update()
        for c in self.clouds:
            c.update()
#class ParallexLayer:
#    def __init__(self, imageName, speed):
#        self.image = load_image(imageName)
#        self.w, self.h = self.image.w, self.image.h
#        self.speed = speed
#
#    def draw(self):
#        self.image.clip_draw_to_origin(self.x1, 0, self.w1, self.h, 0, 0)
#        self.image.clip_draw_to_origin(self.x2, 0, self.w2, self.h, self.w1, 0)
#
#    def update(self, x):
#        self.x1 = int(x * self.speed) % self.image.w
#        self.w1 = self.image.w - self.x1
#
#        self.x2 = 0
#        self.w2 = cw - self.w1 
#
#class ParallexBackground:
#    def __init__(self):
#        self.layers = [\
#            ParallexLayer('res/cloud.jpg', 0.3), \
#            #ParallexLayer('../res/b1.png', 0.7), \
#            #ParallexLayer('../res/b2.png', 1.0), \
#        ]
#        self.min_x, self.min_y = 0, 100
#        self.max_x, self.max_y = 20000, 100,
#        self.x, self.y = 0, 0
#    def clamp(self, o):
#        o.x = clamp(self.min_x, o.x, self.max_x) 
#        o.y = clamp(self.min_y, o.y, self.max_y) 
#    def draw(self):
#        for l in self.layers: l.draw()
#    def update(self):
#        player = racing_state.player
#        for l in self.layers: l.update(self.x)
class Tree:
    image = None
    def __init__(self):
        self.x = random.randint(-100, 100) if random.randint(0,1) else random.randint(cw - 100, cw + 100)
        self.y = random.randint(0, ch)
        if Tree.image == None:
            Tree.image = pico2d.load_image('res/tree.png')
            print('Tree', self.image)
    def draw(self):
        Tree.image.draw(self.x, self.y)
    def update(self):
        player = racing_state.player
        self.y -= 1.5 * player.car.y_speed
        if self.y < 0: self.y += ch
        if self.y > ch: self.y -= ch
        self.x -= player.car.x_speed
        if self.x < 0: self.x += cw
        if self.x > cw: self.x -= cw
class Cloud:
    image = None
    def __init__(self):
        self.x = random.randint(0, cw)
        self.y = random.randint(0, ch)
        if Cloud.image == None:
            Cloud.image = pico2d.load_image('res/cloud.png')
            print('Cloud', self.image)
    def draw(self):
        Cloud.image.draw(self.x, self.y)
    def update(self):
        player = racing_state.player
        self.y -= 2 * player.car.y_speed
        if self.y < 0: self.y += ch
        if self.y > ch: self.y -= ch
        self.x -= 2 * player.car.x_speed
        if self.x < 0: self.x += cw
        if self.x > cw: self.x -= cw