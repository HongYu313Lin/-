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
        self.ball_position_history=[]
        self.ball_destination_1P=98
        filename = "D:\\MLGame-master\\MLGame-master\\games\\pingpong\\ml\\LR_example_1P_right.sav"
        self.model_right = pickle.load(open(filename,'rb'))
        filename = "D:\\MLGame-master\\MLGame-master\\games\\pingpong\\ml\\LR_example_1P_left.sav"
        self.model_left = pickle.load(open(filename,'rb'))

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        
        hit_deep = 1
        ball_destination = 98
        ball_pre = []
            
        if scene_info["status"] != "GAME_ALIVE":
            print(scene_info["ball_speed"])
            return "RESET"

        if not self.ball_served:
            self.ball_served = True
            command = random.choice(["SERVE_TO_LEFT","SERVE_TO_RIGHT"])
            return command
        platform1_edge_x = scene_info["platform_1P"][0]+35
        if scene_info['ball'][1]>420-5-1 and scene_info["ball_speed"][0] > 0 : #當球從 1P 向右出發，預測下一次球回來的位置
            inp_temp = np.array([scene_info["ball"][0]])
            input = inp_temp[np.newaxis, :]
            self.ball_destination_1P = self.model_right.predict(input)
        if scene_info['ball'][1]>420-5-1 and scene_info["ball_speed"][0] < 0 : #當球從 1P 向左出發，預測下一次球回來的位置
            inp_temp = np.array([scene_info["ball"][0]])
            input = inp_temp[np.newaxis, :]
            self.ball_destination_1P = self.model_left.predict(input)
        if self.side == "1P":
#========================================當球往1P移動時，計算球的落點==========================================
#====判斷因為目前計算方式與實際落點有誤差，只能維持到19的速度，若能優化落點計算方式，應該可以撐到更高的速度=========
           if scene_info["ball_speed"][1]>0:
                ball_destination = scene_info["ball"][0]+ (((420-scene_info["ball"][1])/scene_info["ball_speed"][1])*scene_info["ball_speed"][0])
                while ball_destination < 0 or ball_destination > 195:
                    if ball_destination < 0:
                        ball_destination = -ball_destination
                    if ball_destination > 195:
                        ball_destination = 195-(ball_destination-195)

#===================================當球往1P移動時，將板子往計算的落點移動=====================================
                if ball_destination < scene_info["platform_1P"][0]+hit_deep:
                    command = "MOVE_LEFT"
                elif ball_destination > platform1_edge_x-hit_deep:
                    command = "MOVE_RIGHT"
                else:
                    command = "NONE"
                return command
#===================================當球往2P時，將板子往預測的落點移動==========================================
           elif scene_info["ball_speed"][1]<0:
                if self.ball_destination_1P < scene_info["platform_1P"][0]+hit_deep:
                    command = "MOVE_LEFT"
                elif self.ball_destination_1P > platform1_edge_x-hit_deep:
                    command = "MOVE_RIGHT"
                else:
                    command = "NONE"
                return command
    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
        self.ball_destination_1P=98

'''#========================================當球往1P移動時，計算球的落點==========================================
           if scene_info["ball_speed"][1]>0:
                ball_destination = scene_info["ball"][0]+ (((420-scene_info["ball"][1])/scene_info["ball_speed"][1])*scene_info["ball_speed"][0])
                while ball_destination < 0 or ball_destination > 195:
                    if ball_destination < 0:
                        ball_destination = -ball_destination
                    if ball_destination > 195:
                        ball_destination = 195-(ball_destination-195)
'''