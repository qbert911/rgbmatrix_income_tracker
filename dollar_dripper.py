#!/usr/bin/env python3
from os import truncate
import time
import random
from colorama import Fore, Style
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import copy
import operator
import json
import urllib.request
import render
import physics
import ball

MAX_X = 32
MAX_Y = 64
BOARD_NAME = "board-a.txt"
overlooked_cvx = 13 #red flask
overlooked_crv = 7  #blue flask -- crv_daily -- we can only show five units on the flasks
dimmer = True

options = RGBMatrixOptions()
options.rows = MAX_X
options.cols = MAX_Y
#options.gpio_slowdown = 4
#options.pwm_lsb_nanoseconds = 60
#options.pwm_dither_bits=2
#options.brightness = 60 #causes flicker
#options.show_refresh_rate = True
#options.limit_refresh_rate_hz = 200
#options.pwm_bits = 9
#options.scan_mode = 1
#options.hardware_mapping = 'adafruit-hat' 
#options.disable_hardware_pulsing = True
     
def load_board(array2D):
    num_condensors = 0
    condensor_positions = []
    arr = [[0 for _ in range(MAX_Y)] for _ in range(MAX_X)]    
    for y in range(MAX_Y-1,0,-1):
        for x in range(0,MAX_X):
            arr[x][y] = 0 
            if array2D[y][x] == "^": #wall
                arr[x][y] = -1
            elif array2D[y][x] == "q": #wall
                arr[x][y] = -4
            elif array2D[y][x] == "o": #wall
                arr[x][y] = 71                
            elif array2D[y][x] == "*": #condensor
                arr[x][y] = -20
                #if condensor_positions[num_condensors-1] != y + 1:
                this_condensor = [x,y,-20]
                condensor_positions.append(this_condensor) 
                num_condensors = num_condensors + 1
    return arr,num_condensors,condensor_positions

def get_ball_at(x,y,ball_list,starting_position=0):
    for a in range(starting_position,len(ball_list)):
        if x == ball_list[a].x and y == ball_list[a].y:
            return a
    return -1

def check_list(ball_list):
    for a in range(len(ball_list)):
        aball = get_ball_at(ball_list[a].x,ball_list[a].y,ball_list,0)
        if aball > -1 and aball != a:
            print("founda",aball,a,ball_list[a].x,ball_list[a].y,ball_list[aball].x,ball_list[aball].y)
            ball_list[a].color = 55
            ball_list[aball].color = 55
            time.sleep(10)
    return(ball_list)

def main():
    thismatrix = RGBMatrix(options = options)
    mycanvas = thismatrix.CreateFrameCanvas()
    mycanvas.Fill(0,0,0)
    tic = 0
    total_drips = cointracker = 0
    last_drip = t0 = time.perf_counter()
    condensor_positions = []
    ball_list = []
    array2D = []
    with open(BOARD_NAME, 'r') as f:
        for line in f:
            array2D.append(line)
            array2D[-1] = f"{array2D[-1]}                                "

    _,num_condensors,condensor_positions = load_board(array2D)
    target_amount = 40   #dollar coins to be produced in one day

    target_drips_per_day = (target_amount * (10**num_condensors))
    seconds_per_day = 24*60*60
    seconds_between_drips = seconds_per_day / target_drips_per_day

    booster = True  #frontload the system with coins at the start, useful for testing 
    wait_time = 32*2/1000  #seconds per movement tic

    while True:
        #ball_list = check_list(ball_list) #debug to make sure no balls overlap positions
        if tic % 10000 == 0:
           try:
              with urllib.request.urlopen('http://192.168.0.207:6969/pyportal.json') as url:
                  thisarray = json.loads(url.read().decode())
                  target_amount = int(thisarray['dollar_amount']) #dollar coins to be produced in one day
              print('update succeeded')
           except Exception:
              print('update failed')

        arr,_,_ = load_board(array2D)
        arr = render.draw_balls(arr,ball_list)
        arr = render.draw_condensors(arr,condensor_positions)  

        render.draw_canvas(mycanvas, arr, (time.perf_counter()-t0)*dimmer)
        t1,t2=render.draw_tunnels(mycanvas,arr,ball_list)
        mycanvas = thismatrix.SwapOnVSync(mycanvas)

        arr,ball_list,cointracker,condensor_positions,target_amount = physics.do_condensor(arr,ball_list,cointracker,condensor_positions,target_amount)
        arr,ball_list = physics.handle_forces(arr,ball_list)
        ball_list.sort(key=operator.attrgetter('x'))
        ball_list.sort(key=operator.attrgetter('y'),reverse=True)
        t2.sort()
        t1.sort()
        tic = tic + 1

        if target_amount - 1 <= cointracker:
            if booster:
                booster = False
                print("booster off")
            time.sleep(wait_time)
        elif not booster:
                booster = True
                print("booster back on")            

        now = time.perf_counter()
        if (now - last_drip) >= seconds_between_drips or booster:
            total_drips = total_drips + 1
            newball = ball.ball(int(random.random()*5)+(booster*int(random.random()*28)),0,1 + (10*num_condensors))
            ball_list.append(newball)
            last_drip = time.perf_counter() if booster else last_drip + seconds_between_drips
              #print(f"\r {len(ball_list)} {ball_list[0].x} {ball_list[0].y} {ball_list[0].xmo} {ball_list[0].ymo} ")
        print(f"dollars per day target: {target_amount}  condensors: {num_condensors}  positions: {condensor_positions}",end='')
        #print(f"   drips per day: {target_drips_per_day}  tics/drip:{seconds_between_drips / wait_time:4.2f}  wait per tic:{wait_time}   dollars:{sum(i.count(1) for i in arr) + sum(i.count(3) for i in arr) + sum(i.count(5) for i in arr)}/{cointracker}  pennies on board: {sum(i.count(21) for i in arr)}  drips:{total_drips}  tics:{tic}   hours:{(time.perf_counter() - t0) / 3600:.6f}  {last_drip:0f} {now:0f} {booster}",end="\r")
        print(f"{len(t1)} {len(t2)}  {t1}",end="\r")
if __name__ == '__main__':
   main()


