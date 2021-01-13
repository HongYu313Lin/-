"""
The template of the script for the machine learning process in game pingpong
python MLGame.py -i ml_play_LR_1P.py -i ml_play_SVM_2P.py pingpong EASY
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
        # self.ball_position_history=[]
        # self.ball_destination_1P=98
        # filename = "D:\\MLGame-master\\MLGame-master\\games\\pingpong\\ml\\LR_example_1P_right.sav"
        # self.model_right = pickle.load(open(filename,'rb'))
        # filename = "D:\\MLGame-master\\MLGame-master\\games\\pingpong\\ml\\LR_example_1P_left.sav"
        # self.model_left = pickle.load(open(filename,'rb'))
        
        filename = "D:\\MLGame-master\\MLGame-master\\games\\pingpong\\ml\\MLPR_1P.sav"
        self.model_MLPR_1P = pickle.load(open(filename,'rb'))
        filename = "D:\\MLGame-master\\MLGame-master\\games\\pingpong\\ml\\MLPR_2P.sav"
        self.model_MLPR_2P = pickle.load(open(filename,'rb'))
        
        self.posx = -1

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        
        # hit_deep = 1
        # ball_destination = 98
        # ball_pre = []
            
        if scene_info["status"] != "GAME_ALIVE":
            print(scene_info["ball_speed"])
            return "RESET"
        
        ball = scene_info["ball"]
        speed = scene_info["ball_speed"]
        if speed[0]==0:
            if self.side=='1P':
                speed =[-7,-7]
            else:
                speed =[7,7]
            
        if self.side=='1P':
            if speed[1]>0: #往1P
                x,L2 = self.ball_path(ball, speed, self.model_MLPR_2P, 415)
                nx = x
                nx2 = x
                ix = x
                sx = x
            elif speed[1]<0:#往2P
                x,L2 = self.ball_path(ball, speed, self.model_MLPR_1P, 80)
                ball_2p = [x,80]
                srcspeed =abs(speed[1])
                nspeed =[round((speed[1])/L2[0]),-speed[1]]
                n2speed =[round(-(speed[1])/L2[0]),-speed[1]]
                ispeed =[-nspeed[0],nspeed[1]]
                sspeed =[nspeed[0]+3,nspeed[1]]
                
                nx,nL2 = self.ball_path(ball_2p, nspeed, self.model_MLPR_2P, 415)
                nx2,nL22 = self.ball_path(ball_2p, n2speed, self.model_MLPR_2P, 415)
                ix,iL2 = self.ball_path(ball_2p, ispeed, self.model_MLPR_2P, 415)
                sx,sL2 = self.ball_path(ball_2p, sspeed, self.model_MLPR_2P, 415)
                
        elif self.side=='2P':
            if speed[1]>0: #往1P
                x,L2 = self.ball_path(ball, speed, self.model_MLPR_2P, 415)
                ball_2p = [x,415]
                srcspeed =abs(speed[1])
                nspeed =[round((speed[1])/L2[0]),-speed[1]]
                n2speed =[round(-(speed[1])/L2[0]),-speed[1]]
                ispeed =[-nspeed[0],nspeed[1]]
                sspeed =[nspeed[0]+3,nspeed[1]]
                
                nx,nL2 = self.ball_path(ball_2p, nspeed, self.model_MLPR_1P, 80)
                nx2,nL22 = self.ball_path(ball_2p, n2speed, self.model_MLPR_1P, 80)
                ix,iL2 = self.ball_path(ball_2p, ispeed, self.model_MLPR_1P, 80)
                sx,sL2 = self.ball_path(ball_2p, sspeed, self.model_MLPR_1P, 80)
            elif speed[1]<0:#往2P
                x,L2 = self.ball_path(ball, speed, self.model_MLPR_1P, 80)
                nx = x
                nx2 = x
                ix = x
                sx = x
                
                
                
                
                
            
        # if speed[1]>0:
        #     L1 =self.get_line_func(ball, speed)
        #     L2 = self.getl2(L1,speed,415)
        #     x = self.solve_x(L2, 415)
            
        #     if self.side=='2P':
        #         pos =[x,415]
        #         vel =[round((speed[1])/L2[0]),-speed[1]]
        #         L2 =self.get_line_func(pos, vel)
        #         L3 = self.getl2(L2,vel,80)
        #         x = self.solve_x(L3, 80)
            
        # else:
        #     L1 =self.get_line_func(ball, speed)
        #     L2 = self.getl2(L1,speed,80)
        #     x = self.solve_x(L2, 80)
            
        #     if self.side=='1P':
        #         pos =[x,80]
        #         vel =[round((speed[1])/L2[0]),-speed[1]]
        #         L2 =self.get_line_func(pos, vel)
        #         L3 = self.getl2(L2,vel,415)
        #         x = self.solve_x(L3, 415)
            
        # if x not in self.pre:
        #     self.pre.append(x)
        
        if self.side=='1P':
            px = scene_info["platform_1P"][0]+20
            # if ball[1]>=415:
            #     self.pre.append(ball[0])
            #     print(self.pre,ball[1])
            #     self.pre =[] 
        elif self.side=='2P':
            px = scene_info["platform_2P"][0]+20
            # if ball[1]<=80:
            #     self.pre.append(ball[0])
            #     print(self.pre,ball[1])
            #     self.pre =[] 
        data = [self.adj(nx,196),self.adj(nx2,196),self.adj(ix,196),self.adj(sx,196)]
        
        mins = min(data)
        maxs = max(data)
        
        cx =(mins+maxs)/2 + 2.5
        
        #if self.posx == -1 or (ball[1] <=85 and ball[1] >=410):
        self.posx = cx
        
        error = self.posx - px
        
        #print('cx',round(cx),'nx',round(data[0]),'ix',round(data[1]),'sx',round(data[2]),'px',round(px),'ballx',round(ball[0] ))
        
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
        
        

#         if not self.ball_served:
#             self.ball_served = True
#             command = random.choice(["SERVE_TO_LEFT","SERVE_TO_RIGHT"])
#             return command
#         platform1_edge_x = scene_info["platform_1P"][0]+35
#         if scene_info['ball'][1]>420-5-1 and scene_info["ball_speed"][0] > 0 : #當球從 1P 向右出發，預測下一次球回來的位置
#             inp_temp = np.array([scene_info["ball"][0]])
#             input = inp_temp[np.newaxis, :]
#             self.ball_destination_1P = self.model_right.predict(input)
#         if scene_info['ball'][1]>420-5-1 and scene_info["ball_speed"][0] < 0 : #當球從 1P 向左出發，預測下一次球回來的位置
#             inp_temp = np.array([scene_info["ball"][0]])
#             input = inp_temp[np.newaxis, :]
#             self.ball_destination_1P = self.model_left.predict(input)
#         if self.side == "1P":
# #========================================當球往1P移動時，計算球的落點==========================================
# #====判斷因為目前計算方式與實際落點有誤差，只能維持到19的速度，若能優化落點計算方式，應該可以撐到更高的速度=========
#            if scene_info["ball_speed"][1]>0:
#                 ball_destination = scene_info["ball"][0]+ (((420-scene_info["ball"][1])/scene_info["ball_speed"][1])*scene_info["ball_speed"][0])
#                 while ball_destination < 0 or ball_destination > 195:
#                     if ball_destination < 0:
#                         ball_destination = -ball_destination
#                     if ball_destination > 195:
#                         ball_destination = 195-(ball_destination-195)

# #===================================當球往1P移動時，將板子往計算的落點移動=====================================
#                 if ball_destination < scene_info["platform_1P"][0]+hit_deep:
#                     command = "MOVE_LEFT"
#                 elif ball_destination > platform1_edge_x-hit_deep:
#                     command = "MOVE_RIGHT"
#                 else:
#                     command = "NONE"
#                 return command
# #===================================當球往2P時，將板子往預測的落點移動==========================================
#            elif scene_info["ball_speed"][1]<0:
#                 if self.ball_destination_1P < scene_info["platform_1P"][0]+hit_deep:
#                     command = "MOVE_LEFT"
#                 elif self.ball_destination_1P > platform1_edge_x-hit_deep:
#                     command = "MOVE_RIGHT"
#                 else:
#                     command = "NONE"
#                 return command

    #mlpr
    def ball_path(self,pos,vel,model,y):
        L1 =self.get_line_func(pos, vel)
        L1 =(L1[0],L1[1]/415)
        L2 = model.predict([L1])[0]
        L2 =(L2[0],L2[1]*415)
        x = self.solve_x(L2, y)
        return x,L2
    #rulebase
    # def ball_path_sim(self,pos,vel,model,y):
    #     L1 =self.get_line_func(pos, vel)
    #     #L1 =(L1[0],L1[1]/415)
    #     L2 = self.getl2( L1,vel,y)
    #     #L2 =(L2[0],L2[1]*415)
    #     x = self.solve_x(L2, y)
    #     return x,L2
        
    def get_line_func(self,pos,vel):
        a = vel[1]/vel[0]
        b = pos[1]-a*pos[0]
        return a,b
    
    def solve_x(self,line,y):
        x = (y-line[1])/line[0]
        return x
    
    def adj(self,posx,maxx):
        q = (abs(posx)//(maxx))
        mod =(abs(posx)%(maxx))
        q2 =q%2
        if q2 ==1:
            mod = maxx-mod
        newx = mod
        return newx
    
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
    
    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
        self.posx = -1

'''#========================================當球往1P移動時，計算球的落點==========================================
           if scene_info["ball_speed"][1]>0:
                ball_destination = scene_info["ball"][0]+ (((420-scene_info["ball"][1])/scene_info["ball_speed"][1])*scene_info["ball_speed"][0])
                while ball_destination < 0 or ball_destination > 195:
                    if ball_destination < 0:
                        ball_destination = -ball_destination
                    if ball_destination > 195:
                        ball_destination = 195-(ball_destination-195)
'''