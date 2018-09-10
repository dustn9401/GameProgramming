# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 10:45:01 2018

@author: kys
"""

from turtle import *

def move(x,y):
    pu()
    goto(x,y)
    pd()
    
#김
move(-200,100)
seth(0)
forward(100)
right(120)
forward(120)
move(-80, 120)
seth(270)
forward(120)
seth(180)
forward(70)
seth(270)
forward(50)
seth(0)
forward(70)
seth(90)
forward(50)

#연
move(70,70)
circle(40)
move(100,120)
seth(270)
forward(120)
move(100,80)
seth(180)
forward(40)
move(100,40)
seth(180)
forward(50)

#수
move(30, 0)
seth(270)
forward(50)
seth(0)
forward(80)

move(200,100)
seth(225)
forward(100)
move(200,100)
seth(315)
forward(100)
move(120, 20)
seth(0)
forward(200)
move(220, 20)
seth(270)
forward(80)

done()
    