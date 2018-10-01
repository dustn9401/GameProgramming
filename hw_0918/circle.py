# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 16:25:49 2018

@author: kys
"""

import turtle

def draw_circle(x,y,r):
    turtle.seth(0)
    turtle.pu()
    turtle.goto(x,y)
    turtle.stamp()
    turtle.goto(x,y-r)
    turtle.pd()
    turtle.circle(r)
    
turtle.shape("turtle")
draw_circle(0,0,50)
draw_circle(200,200,100)
draw_circle(100,-100,50)

turtle.done()