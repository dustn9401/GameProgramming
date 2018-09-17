from pico2d import *
import math
open_canvas()

grass = load_image('grass.png')
character = load_image('run_animation.png')

x = 0
y=0
frame=0
right,up,left,down,circle=1,2,3,4,5  #방향 나타낼 변수
where=1                                 #현재 방향을 나타낼 변수
angle=(3*math.pi)/2             # θ = 3/2π 
cnt=0
while (True):
        clear_canvas()
        grass.draw(400, 30)
        character.clip_draw(frame*100, 0, 100,100,x,y)
        update_canvas()

        frame=(frame+1)%8		

        if where==right:
                if x<800:
                        x+=10
                else:
                        where=up
        elif where==up:
                if y<600:
                        y+=10
                else:
                        where=left
        elif where==left:
                if x>0:
                        x-=10
                else:
                        where=down
        elif where==down:
                if y>0:
                        y-=10
                else:
                        if x<400:       #아래 방향일 때 오른쪽으로도 중간까지 감
                                x+=10
                        else:
                                where=circle
        elif where==circle:
                if cnt<360:     #360도를 다 회전하지 않았다면
                        x=400+300*math.cos(angle)       #x=400+rcosθ
                        y=300+300*math.sin(angle)       #y=300+rsinθ
                        cnt+=1                          #360도 회전시키기 위한 카운터
                        angle = angle + (math.pi/180)   #파이썬 삼각함수는 라디안법을 사용함
                else:           #회전 완료이면
                        cnt=0
                        angle=(3*math.pi)/2     #θ = 3/2π 
                        where=right
                
        delay(0.01)
        get_events()
    
close_canvas()
