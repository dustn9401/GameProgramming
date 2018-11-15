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
        self.y = 0
        self.dx = 0
    def draw(self):
        Road.image.clip_draw_to_origin(int(self.x), int(self.y), cw, ch, 0, 0)
    def update(self):
        player = racing_state.player
        cars = racing_state.cars
        self.y += player.car.y_speed
        if self.y > Road.image.h - ch: self.y = 0
        if self.y < 0: self.y = ch//2
        #self.x = pico2d.clamp(cw - Road.image.w//2, self.x + player.car.x_speed, Road.image.w//2)
        tx = self.x
        self.x = pico2d.clamp(0, self.x + player.dx, Road.image.w - cw)
        self.dx = self.x - tx
        
        for c in cars:
            c.x -= self.dx
        
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
        road = racing_state.bg.road
        if self.x == None:
            self.x = random.randint(-100-road.x, -road.x) if random.randint(0,1) else random.randint(Road.image.w - road.x - 200 - 50, Road.image.w - road.x - 200 + 50)
        self.x -= road.dx
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
        road = racing_state.bg.road
        self.x -= 0.01 * road.dx
        self.y -= 0.1 * player.car.y_speed
        if self.y < 0: 
            self.y += ch
            self.x = random.randint(0, cw)
        if self.y > ch: 
            self.y -= ch
            self.x = random.randint(0, cw)
        