#!/usr/bin/env python3
import time
import random
MAX_X = 32
MAX_Y = 64

class ball:
    def __init__(self,x,y,color):
        self.color = color
        self.color_previous = color
        self.x = x
        self.y = y
        self.xmo = 0
        self.ymo = 0
        self.spawn_time = time.perf_counter()
        self.intunnel = 0
        self.tunnelis = 0
        
    def incrementx(self,amount):
        if self.xmo != 0:
            self.xmo += amount
        else:
            self.xmo = amount

        return self.xmo

    def decrementx(self,amount=1):
        if self.xmo < 0:
            self.xmo += amount
        elif self.xmo > 0:
            self.xmo -= amount
        return self.xmo

    def gravity(self,amount=1):
        self.ymo = max(self.ymo+amount,0)

    def move(self,x,y):
        self.x += x
        self.y += y

        if self.x == MAX_X -1 and self.y == 25: #wraparound wormhole
            self.color_previous = self.color
            self.color = 0 
            self.tunnelis = 1
            self.intunnel = 11+2
            self.x = int(random.random()*0)+17
            self.y = 24
        elif self.x == 0 and self.y == 63: #wraparound wormhole
            self.color_previous = self.color
            self.color = 0 
            self.tunnelis = 2
            self.intunnel = 63 - 11
            self.x = int(random.random()*0)+0
            self.y = 11
        elif (self.x == MAX_X -1 and self.y == 24) or\
           (self.x == 0 and self.y == 62): #flash purple when next to wormhole 
            self.color = 60


    def left(self,arr):
       return arr[self.x-1][self.y+0] if self.x > 0 else -1
    def right(self,arr):
       return arr[self.x+1][self.y+0] if self.x < MAX_X - 1 else -1
    def up(self,arr):
        return arr[self.x][self.y-1] if self.y > 0 else -1
    def upleft(self,arr):
        return arr[self.x-1][self.y-1]  if self.y > 0 and self.x > 0 else -1
    def upright(self,arr):
        return arr[self.x+1][self.y-1] if self.y > 0 and self.x < MAX_X -1 else -1
    def down(self,arr):
        return arr[self.x][self.y+1] if self.y < MAX_Y -1 else -1
    def downleft(self,arr):
        return arr[self.x-1][self.y+1] if self.y < MAX_Y -1 and self.x > 0 else -1
    def downright(self,arr):
        return arr[self.x+1][self.y+1] if self.y < MAX_Y -1 and self.x < MAX_X - 1 else -1
