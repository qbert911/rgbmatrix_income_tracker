#!/usr/bin/env python3
import random
import json
import urllib.request
import operator
import ball
MAX_X = 32
MAX_Y = 64
    
def do_condensor(arr2,ball_list,cointracker,condensor_positions,target_amount):
    for a in range(len(ball_list)-1,-1,-1):
        x=ball_list[a].x
        y=ball_list[a].y
        for b in range(len(condensor_positions)):
            if condensor_positions[b][2] == -10 and arr2[condensor_positions[b][0]][condensor_positions[b][1]+1] < -10:
                condensor_positions[b][2] = -20 #reset condensor
                condensor_positions[b-1][2] = condensor_positions[b-1][2]+1   #increase condensor count
            elif condensor_positions[b][2] == -10 and arr2[condensor_positions[b][0]][condensor_positions[b][1]+1] == 0:
                condensor_positions[b][2] = -20 #reset condensor
                if b > 0:               
                    this_droplet = (b*10)+1   #change to next level ball color
                else:                 
                    cointracker = cointracker + 1
                    arr2,ball_list,cointracker,target_amount = handle_decay(arr2,ball_list,cointracker,target_amount)
                    this_droplet = 1
                    if cointracker % 20 == 0:  #change final ball color every 20 and 100 balls
                        this_droplet = 3
                    if cointracker % 100 == 0:
                        this_droplet = 5

                ball_list.append(ball.ball(condensor_positions[b][0],condensor_positions[b][1],this_droplet)) #extrude new ball out after condensor fills up 

            elif condensor_positions[b][0] in [x,x-1,x+1] and condensor_positions[b][1] == y+1: #spot above is occupied
                condensor_positions[b][2] = condensor_positions[b][2]+1  #increase condensor count
                del ball_list[a]

    return arr2,ball_list,cointracker,condensor_positions,target_amount

def handle_decay(arr,ball_list,cointracker,target_amount_in):
    #dollarsonboard = sum([i.count(1) for i in arr])+sum([i.count(3) for i in arr])+sum([i.count(5) for i in arr])
    try:
        thisarray = json.loads(urllib.request.urlopen('http://192.168.0.207:6969/pyportal.json').read().decode())
        target_amount = int(thisarray['dollar_amount']) #dollar coins to be produced in one day
    except Exception:
        print("error fetching")
        target_amount = target_amount_in

    left_to_trim = cointracker - target_amount
    if left_to_trim > 0:
        #ball_list.sort(key=operator.attrgetter('y'),reverse=True)
        ball_list.sort(key=operator.attrgetter('spawn_time'))
        for a in range(len(ball_list)-1,-1,-1):
            if left_to_trim > 0 and ball_list[a].color < 11 and ball_list[a].color > 0:
                #print("\ndeleting",ball_list[a].x,ball_list[a].y,cointracker, target_amount)
                del ball_list[a]
                cointracker -= 1
                left_to_trim -= 1
    return arr,ball_list,cointracker,target_amount

def handle_forces(arr,ball_list):
    for a in range(len(ball_list)):
        x=ball_list[a].x
        y=ball_list[a].y
        xmo=ball_list[a].xmo
        ymo=ball_list[a].ymo
        upleft = ball_list[a].upleft(arr)
        up = ball_list[a].up(arr)
        upright = ball_list[a].upright(arr)
        downleft = ball_list[a].downleft(arr)
        down = ball_list[a].down(arr)
        downright = ball_list[a].downright(arr)
        left=ball_list[a].left(arr)
        right=ball_list[a].right(arr)
        intunnel=ball_list[a].intunnel

        if ball_list[a].color == 60:        #flip back
            ball_list[a].color = ball_list[a].color_previous

        if intunnel > 1:
            ball_list[a].intunnel = ball_list[a].intunnel - 1
        elif intunnel == 1:
            ball_list[a].intunnel = 0
            ball_list[a].color = 60
        elif abs(xmo) > abs(ymo): #try to move sideways first
            if xmo > 0 and right == 0:
                ball_list[a].move(+1,+0)
                arr[x+1][y+0] = arr[x][y] 
                arr[x][y] = 0 
                ball_list[a].decrementx()
                print("r",ball_list[a].x,ball_list[a].y)      
            elif xmo < 0 and left == 0:
                ball_list[a].move(-1,+0)
                arr[x-1][y+0] = arr[x][y] 
                arr[x][y] = 0 
                ball_list[a].decrementx()
                print("l",ball_list[a].x,ball_list[a].y)
            #if down == 0:
                #ball_list[a].gravity()  #if shooting over open air, apply gravity
        elif down == 0:
                ball_list[a].move(+0,+1)
                arr[x+0][y+1] = arr[x][y] 
                arr[x][y] = 0 
                ball_list[a].gravity()
                ball_list[a].decrementx()
        elif downleft == 0 and downright == 0:
            if int(random.random()*2) == 1:
                ball_list[a].move(-1,+1)
                arr[x-1][y+1] = arr[x][y] 
                arr[x][y] = 0 
                ball_list[a].gravity()
                ball_list[a].incrementx(-1)
            else:
                ball_list[a].move(+1,+1)
                arr[x+1][y+1] = arr[x][y] 
                arr[x][y] = 0 
                ball_list[a].gravity()
                ball_list[a].incrementx(+1)
        elif downright == 0:
                ball_list[a].move(+1,+1)
                arr[x+1][y+1] = arr[x][y] 
                arr[x][y] = 0 
                ball_list[a].gravity()
                ball_list[a].incrementx(+1)
        elif downleft == 0:
                ball_list[a].move(-1,+1)
                arr[x-1][y+1] = arr[x][y] 
                arr[x][y] = 0 
                ball_list[a].gravity()
                ball_list[a].incrementx(-1)
        elif xmo > 0 and right == 0: #past this point there are no empties below us 
                ball_list[a].move(+1,+0)
                arr[x+1][y+0] = arr[x][y] 
                arr[x][y] = 0 
                ball_list[a].decrementx()
                ball_list[a].gravity(-1)
        elif xmo < 0 and left == 0:
                ball_list[a].move(-1,+0)
                arr[x-1][y+0] = arr[x][y] 
                arr[x][y] = 0 
                ball_list[a].decrementx()
                ball_list[a].gravity(-1)  
        #elif right == 0 and left == 0 and ymo > 1:  
        #    if int(random.random()*2) == 1:
        #        ball_list[a].move(-1,+0)
        #        arr[x-1][y+0] = arr[x][y] 
        #        arr[x][y] = 0 
        #        ball_list[a].gravity(-1)
        #        ball_list[a].incrementx(-1)
        #    else:
        #        ball_list[a].move(+1,+0)
        #        arr[x+1][y+0] = arr[x][y] 
        #        arr[x][y] = 0 
        #        ball_list[a].gravity(-1)
        #        ball_list[a].incrementx(+1)
        elif right == 0 and left == 0 and up > 1:  #ball directly on top of us
            if int(random.random()*2) == 1:
                ball_list[a].move(-1,+0)
                arr[x-1][y+0] = arr[x][y] 
                arr[x][y] = 0 
                ball_list[a].gravity(-1)
            else:
                ball_list[a].move(+1,+0)
                arr[x+1][y+0] = arr[x][y] 
                arr[x][y] = 0 
                ball_list[a].gravity(-1)
        elif right == 0 and upleft > 1 and left != 0:
                ball_list[a].move(+1,+0)
                arr[x+1][y+0] = arr[x][y] 
                arr[x][y] = 0 
                ball_list[a].gravity(-1)
        elif left == 0 and upright > 1 and right != 0:
                ball_list[a].move(-1,+0)
                arr[x-1][y+0] = arr[x][y] 
                arr[x][y] = 0 
                ball_list[a].gravity(-1)
        elif xmo > 0 and right == 0:
                ball_list[a].move(+1,+0)
                arr[x+1][y+0] = arr[x][y] 
                arr[x][y] = 0 
                ball_list[a].decrementx()
        elif xmo < 0 and left == 0:
                ball_list[a].move(-1,+0)
                arr[x-1][y+0] = arr[x][y] 
                arr[x][y] = 0 
                ball_list[a].decrementx()
        #else:
        #    ball_list[a].decrementx()
        #    ball_list[a].gravity(-1)

    return arr,ball_list