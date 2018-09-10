from turtle import *
import random

colormode(255)      #색깔 모드설정, 디폴트는 0이상 1미만

def tree(x, y, level, head):
    if level == max_level:
        return
    
    goto(x,y)
    speed(0) #속도 제일빠르게
    pensize(max_level-level)     #펜 두께 설정
    
    rgb = [level*20,level*20,0]   #색깔, 0이 제일 어두움
    color(rgb)    
    
    length = random.randrange(180,220)/(2**((level)/1.5)) #가지의 길이
    seth(head)
    
    pd()
    forward(length)

    color("green")
    stamp()
    pu()
    
    cur_x, cur_y = xcor(), ycor()
    tree(cur_x, cur_y, level+1, head+random.randrange(20,40))
    tree(cur_x, cur_y, level+1, head-random.randrange(20,40))

max_level=7
pu()
tree(0, -300, 0, 90)
done()