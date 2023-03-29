#!/usr/bin/env python3
MAX_X = 32
MAX_Y = 64

def draw_canvas(thiscanvas,arr,tic):
   for y in range(MAX_Y):
        for x in range(MAX_X):
            r,g,b = this_pixel(arr[x][y],tic)
            thiscanvas.SetPixel(y, MAX_X-1-x, r, g, b)

def draw_tunnels(thiscanvas,arr,ball_list):
    t1=[]
    t2=[]
    for a in range(len(ball_list)):
        if ball_list[a].intunnel > 0:
            if ball_list[a].tunnelis == 1:
                t1.append(ball_list[a].intunnel)
            elif ball_list[a].tunnelis == 2:
                t2.append(ball_list[a].intunnel)   
    r,g,b = 26,2,36   
    if arr[0][62] == 0:    
        thiscanvas.SetPixel(62, MAX_X-1-0, r, g, b)
    if arr[31][24] == 0:    
        thiscanvas.SetPixel(24, MAX_X-1-31, r, g, b)
   
    for a in range(30,16,-1):
        if arr[a][24] == 0 or arr[a][24] == -4:
            if a-17 in t1:
                r1,g1,b1 = 25,10,15
            else:
                r1,g1,b1 = 1,2,2
            thiscanvas.SetPixel(24, MAX_X-1-a, r1, g1, b1)
    for a in range(61,10,-1):
        if arr[0][a] == 0 or arr[0][a] == -4:
            if a-10 in t2:
                r2,g2,b2 = 25,10,15
            else:
                r2,g2,b2 = 1,2,2
            thiscanvas.SetPixel(a, MAX_X-1-0, r2, g2, b2)            
    return t1,t2

def this_pixel(input,tic):
    if input == 0:
        return 0,0,0
    if input == 1:  #dollar
        return 5,60,5
    elif input == 11:  #dime
        return 20,30,40
    elif input == 21:  #penny
        return 100,50,10
    elif input == 31:  #deci-penny
        return 90,90,25
    elif input == -2:
        return max(0,int(40-tic)),max(0,int(40-tic)),max(0,int(40-tic)) # 134,134,12
    elif input == 3: #twenty dollars 
        return 0,130,0
    elif input == 5: #one hundred dollars
        return 70,0,0
    elif input == -1:        
        #if tic > 1000:
        #    return 0,0,0 # 10,20,20
        return max(0,int(40-tic)),max(0,int(40-tic)),max(0,int(40-tic)) # 10,20,20
    elif input <= -10:
        #return (input+20)*20,0,(input+20)*10
        #if int(random.random()*40) == 1:  #add twinkle
        #    return (input+20)*10,(input+20)*15,(input+20)*22
        #else:
            return 0,(input+20)*10,(input+20)*20
    elif input == 60:
        return 65,5,90  
    elif input == 70:
        return 5,5,90
    elif input == 71:
        return 0,0,40
    elif input == 80:
        return 90,5,5
    elif input == -3:
        return 20,30,44
        #return 1,2,2
        #return 0,0,0
    elif input == -4:
        return 5,10,10
        #return 0,0,0
    else:
        return 255,0,255

def draw_balls(arr,ball_list):
    for a in range(len(ball_list)):
        #print(ball_list[a].x,ball_list[a].y)
        if arr[ball_list[a].x][ball_list[a].y] == 0:
            if ball_list[a].intunnel == 0:
                arr[ball_list[a].x][ball_list[a].y] = ball_list[a].color
    return arr

def draw_condensors(arr,condensor_positions):
    for a in range(len(condensor_positions)):
        arr[condensor_positions[a][0]][condensor_positions[a][1]] = condensor_positions[a][2]
    return arr
