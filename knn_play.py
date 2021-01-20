# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 17:54:40 2020

@author: HQHQH
"""
"""
The template of the main script of the machine learning process
"""
from sklearn.neighbors import KNeighborsClassifier 
from sklearn.neural_network import MLPClassifier
import pickle
import numpy as np

# model_name = r"D:\MLGame-master\MLGame-master\KNN_model.sav"
# f = open(model_name,'rb')
# KNN_model = pickle.load(f)

class MLPlay:
    def __init__(self, side):
        """
        Constructor
        """
        self.ball_served = False
        self.ball_position =[]
        self.end_position =[]
        self.side = side

    def update(self, scene_info):
        """
        Generate the command according to the received `scene_info`.
        """
        #show scene_info content
        
        #print (scene_info['ball'])
        
        # Make the caller to invoke `reset()` for the next round.
        if scene_info["status"] != "GAME_ALIVE":
            self.reset()
            return "RESET"
        
        platform_position = np.array(scene_info['platform'])
        self.ball_position.append(scene_info["ball"])
        
        if self.side =='1P':
            if self.ball_position[-1][1]>=414:
                self.end_position.append(self.ball_position[-1])
        elif self.side =='2P':
            if self.ball_position[-1][1]<=81:
                self.end_position.append(self.ball_position[-1])
        
            
        eigen_vector =  np.array(self.ball_position)
        tmppos = np.array(self.end_position)
        eigen_label = np.array(tmppos[:,0])
        
        #----------------knn---------------
        # data_train = KNeighborsClassifier()
        # data_train.fit(eigen_vector, eigen_label)
        # model_name = "KNN_model.sav"
        # pickle.dump(data_train, open(model_name, 'wb'))
        
        # model_name = r"D:\MLGame-master\MLGame-master\KNN_model.sav"
        # f = open(model_name,'rb')
        # KNN_model = pickle.load(f)
        
        # balls = np.array(self.ball_position)
        # predict = KNN_model.predict(balls)
        
        #----------------mlp---------------
        X_train = eigen_vector
        y_train = eigen_label
        mlp = MLPClassifier(hidden_layer_sizes=(50,), max_iter=10, alpha=1e-4,
                    solver='sgd', verbose=10, tol=1e-4, random_state=1,
                    learning_rate_init=.1)
        
        mlp.fit(X_train, y_train)
        model_name = "MLP_model.sav"
        pickle.dump(mlp, open(model_name, 'wb'))
        
        model_name = r"D:\MLGame-master\MLGame-master\MLP_model.sav"
        f = open(model_name,'rb')
        MLP_model = pickle.load(f)
        
        balls = np.array(self.ball_position)
        predict = MLP_model.predict(balls)
        
        
        
        
        
        
        
        if not self.ball_served:
            
            predict[0] = 45
            
            if platform_position[0] < predict[0]:
                command = "MOVE_RIGHT"
            elif platform_position[0] > predict[0]:
                command = "MOVE_LEFT"
            elif platform_position[0] == predict[0]:
                self.ball_served = True
                command = "SERVE_TO_LEFT"
            
        else:
            
            
            #print (scene_info['ball'] ," , ",predict," , ",platform_position)
            
            if platform_position[0] < predict[0]:
                command = "MOVE_RIGHT"
            elif platform_position[0] > predict[0]:
                command = "MOVE_LEFT"
            elif platform_position[0] == predict[0]:
                command = "NONE"
            
            
            #command = "MOVE_RIGHT" 

        return command

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
        self.ball_position =[]
        self.end_position =[]