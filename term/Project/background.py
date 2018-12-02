# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 17:32:39 2018

@author: kys
"""

import racing_state
import pico2d
import random
import base
cw = 800
ch = 600
TREE = 100
CLOUD = 2
class Background:
    def __init__(self):
        self.road = Road()
        self.trees = [Tree() for i in range(TREE)]
        self.clouds = [Cloud() for i in range(CLOUD)]
    def draw(self):
        self.road.draw()
        for t in self.trees: t.draw()
#        for c in self.clouds: c.draw()         #마지막에그림
    def update(self):
        self.road.update()
        for t in self.trees:
            t.update()
        for c in self.clouds:
            c.update()

class Road(base.BaseObject):
    image = None
    def __init__(self):
        if Road.image == None:
            Road.image = pico2d.load_image('res/img/road.png')
            print('Road', self.image)
        self.x = Road.image.w//2
        self.y = Road.image.h//2
        self.y_lower = -ch
        self.y_upper = ch
        self.dx = 0
    def draw(self):
#        Road.image.clip_draw_to_origin(int(self.x), int(self.y_lower), cw, ch, 0, 0)
#        Road.image.clip_draw_to_origin(int(self.x), int(self.y), cw, ch, 0, 0)
#        Road.image.clip_draw_to_origin(int(self.x), int(self.y_upper), cw, ch, 0, 0)
        Road.image.draw(cw//2, self.y_lower, cw, ch)
        Road.image.draw(cw//2, self.y, cw, ch)
        Road.image.draw(cw//2, self.y_upper, cw, ch)
    def update(self):
        player = racing_state.player
        self.y -= player.car.y_speed
        if self.y_lower < -ch//2:
            self.y += ch
        if self.y_upper > ch//2:
            self.y -= ch
        self.y_lower = self.y - ch + 10
        self.y_upper = self.y + ch - 10
        
class Tree(base.BaseObject):
    image = None
    def __init__(self):
        self.x = None
        self.y = random.randint(0, ch)
        if Tree.image == None:
            Tree.image = pico2d.load_image('res/img/tree.png')
            print('Tree', self.image)
    def draw(self):
        Tree.image.draw(self.x, self.y)
    def update(self):
        player = racing_state.player
        if self.x == None:
            self.x = random.randint(0, 100) if random.randint(0,1) else random.randint(cw - 100, cw)
        self.y -= player.car.y_speed
        if self.y < 0: self.y += ch
        if self.y > ch: self.y -= ch
        
class Cloud(base.BaseObject):
    image = None
    def __init__(self):
        self.x = random.randint(0, cw)
        self.y = random.randint(0, ch)
        if Cloud.image == None:
            Cloud.image = pico2d.load_image('res/img/cloud.png')
            print('Cloud', self.image)
    def draw(self):
        Cloud.image.draw(self.x, self.y)
    def update(self):
        player = racing_state.player
        self.y -= 0.1 * player.car.y_speed
        if self.y < 0: 
            self.y += ch
            self.x = random.randint(0, cw)
        if self.y > ch: 
            self.y -= ch
            self.x = random.randint(0, cw)
        