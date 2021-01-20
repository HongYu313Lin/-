# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 11:26:59 2021

@author: HQHQH
"""
import random
import math
import pickle
import numpy as np

class MLPlay:
    def __init__(self, side):
        """
        Constructor
        @param side A string "1P" or "2P" indicates that the `MLPlay` is used by
               which side.
        """
        self.ball_served = False
        self.side = side
        self.pre =[]

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        if scene_info["status"] != "GAME_ALIVE":
            print(scene_info["ball_speed"])
            self.reset()
            return "RESET"
        
        
        ball = scene_info["ball"]
        speed = scene_info["ball_speed"]
        if speed[0]==0:
            speed =[7,7]
            
        if speed[1]>0:
            L1 =self.get_line_func(ball, speed)
            L2 = self.getl2(L1,speed,415)
            x = self.solve_x(L2, 415)
            
            if self.side=='2P':
                pos =[x,415]
                vel =[round((speed[1])/L2[0]),-speed[1]]
                L2 =self.get_line_func(pos, vel)
                L3 = self.getl2(L2,vel,80)
                x = self.solve_x(L3, 80)
            
        else:
            L1 =self.get_line_func(ball, speed)
            L2 = self.getl2(L1,speed,80)
            x = self.solve_x(L2, 80)
            
            if self.side=='1P':
                pos =[x,80]
                vel =[round((speed[1])/L2[0]),-speed[1]]
                L2 =self.get_line_func(pos, vel)
                L3 = self.getl2(L2,vel,415)
                x = self.solve_x(L3, 415)
            
        if x not in self.pre:
            self.pre.append(x)
        
        if self.side=='1P':
            px = scene_info["platform_1P"][0]+20
            if ball[1]>=415:
                self.pre.append(ball[0])
                print(self.pre,ball[1])
                self.pre =[] 
        elif self.side=='2P':
            px = scene_info["platform_2P"][0]+20
            if ball[1]<=80:
                self.pre.append(ball[0])
                print(self.pre,ball[1])
                self.pre =[] 
        
        cx =x+2.5
        error = cx-px
        
        if scene_info["ball_speed"][0]!=0 and not self.ball_served:
            self.ball_served = True

        if not self.ball_served:
            error = 45-px
            if error > 3:
                command = "MOVE_RIGHT"
            elif error < -3:
                command = "MOVE_LEFT"
            else:
                self.ball_served = True
                #command = random.choice(["SERVE_TO_LEFT","SERVE_TO_RIGHT"])
                command = "SERVE_TO_LEFT"
            return command
        else:
            if error > 3:
                command = "MOVE_RIGHT"
            elif error < -3:
                command = "MOVE_LEFT"
            else:
                command = "NONE"
        return command
        
       
    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
        self.pre =[]
        
    def get_line_func(self,pos,vel):
        a = vel[1]/vel[0]
        b = pos[1]-a*pos[0]
        return a,b
    
    def solve_x(self,line,y):
        x = (y-line[1])/line[0]
        return x
    
    def limmit(self,posx,velx,maxx):
        q = (abs(posx)//(maxx))
        mod =(abs(posx)%(maxx))
        q2 =q%2
        v = abs(velx)
        if q2 ==1:
            mod = maxx-mod
            v=-abs(velx)
        newx = mod
        if q!=0:
            newv = v
        else:
            newv = velx
        return newx,newv
    
    def getl2(self,line,vel, y):
        x = self.solve_x(line, y)
        newx,newv = self.limmit( x, vel[0], 195)
        pos = [newx,y]
        vel = [newv,vel[1]]
        L2 =self.get_line_func(pos, vel)
        return L2
