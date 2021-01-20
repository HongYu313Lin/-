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
from sklearn.neural_network import MLPRegressor 
import pickle
import numpy as np
import os
import csv

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
        self.starts_position =[]
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
        
        lens = len(self.end_position)
        
        
        self.ball_position.append(scene_info["ball"])
        
        if self.side =='1P':
            platform_position = np.array(scene_info['platform_1P'])
            if self.ball_position[-1][1]>=414:
                tmp =[]
                l = len(self.ball_position)
                for i in range(0,50):
                    if len(self.ball_position)>i:
                        tmp.append(self.ball_position[l-i-1][0]/200)
                        tmp.append(self.ball_position[l-i-1][1]/420)
                    else:
                        tmp.append(self.ball_position[0][0]/200)
                        tmp.append(self.ball_position[0][1]/420)
                
                for i in range(0,50,2):
                    tmps = tmp[i:]
                    if len(tmps)<100:
                        tmps.extend(0 for _ in range(100-len(tmps)))
                    self.starts_position.append(tmps)
                    self.end_position.append([self.ball_position[-1][0]/200,self.ball_position[-1][1]/420])
        
                        
        elif self.side =='2P':
            platform_position = np.array(scene_info['platform_2P'])
            if self.ball_position[-1][1]<=81:
                
                tmp =[]
                l = len(self.ball_position)
                for i in range(0,50):
                    if len(self.ball_position)>i:
                        tmp.append(self.ball_position[l-i-1][0]/200)
                        tmp.append(self.ball_position[l-i-1][1]/420)
                    else:
                        tmp.append(0)
                        tmp.append(0)
                
                for i in range(0,50,2):
                    tmps = tmp[i:]
                    if len(tmps)<100:
                        
                        tmps.extend(0 for _ in range(100-len(tmps)))
                    self.starts_position.append(tmps)
                    self.end_position.append([self.ball_position[-1][0]/200,self.ball_position[-1][1]/420])
        
        if len(self.end_position)>lens:
            #print('starts_position:',len(self.starts_position[0]),'end_position:',len(self.end_position[0]))
            eigen_vector =  np.array(self.starts_position)
            eigen_label = np.array(self.end_position)
            
            
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
            name ='mlp_x_' + self.side + 'logs.csv'
            with open(name, 'a', newline='') as csvfile:
                # 建立 CSV 檔寫入器
                writer = csv.writer(csvfile)
                # 寫入一列資料
                lens =len(X_train)
                for i in range(lens):
                    writer.writerow(X_train[i])
            
            name ='mlp_y_' + self.side + 'logs.csv'
            with open(name, 'a', newline='') as csvfile:
                # 建立 CSV 檔寫入器
                writer = csv.writer(csvfile)
                # 寫入一列資料
                lens =len(y_train)
                for i in range(lens):
                    writer.writerow(y_train[i])
    
            # print('lenX_train',len(X_train),'leny_train',len(y_train))
            
            # for i in range(len(X_train)):
            #     print('x ',len(X_train[i]),' y ',len(y_train[i]))
                
            
            model_name = r"D:\MLGame-master\MLGame-master\MLP_model.sav"
            if os.path.isfile(model_name):
                f = open(model_name,'rb')
                MLP_model = pickle.load(f)
                MLP_model.partial_fit(X_train, y_train)
                
                model_name_sav = "MLP_model.sav"
                pickle.dump(MLP_model, open(model_name_sav, 'wb'))
            else:
                
                namex ='mlp_x_' + self.side + 'logs.csv'
                namey ='mlp_y_' + self.side + 'logs.csv'
                if os.path.isfile(namex) and os.path.isfile(namey):
                    with open(namex, newline='') as csvfile:
                        # 以冒號分隔欄位，讀取檔案內容
                        rows = csv.reader(csvfile)
                        X_train = rows
                    with open(namey, newline='') as csvfile:
                        # 以冒號分隔欄位，讀取檔案內容
                        rows = csv.reader(csvfile)
                        y_train = rows
                
                MLP_model =  MLPRegressor(solver='adam', alpha=1e-5, 
                                          hidden_layer_sizes=(100, ), random_state=1) 
                MLP_model.fit(X_train, y_train)
                model_name_sav = "MLP_model.sav"
                pickle.dump(MLP_model, open(model_name_sav, 'wb'))
                
            tmp =[]
            l = len(self.ball_position)
            for i in range(0,50):
                if len(self.ball_position)>i:
                    tmp.append(self.ball_position[l-i-1][0]/200)
                    tmp.append(self.ball_position[l-i-1][1]/420)
                else:
                    tmp.append(0)
                    tmp.append(0)
            
           
            balls = np.array(tmp)
            predict = MLP_model.predict([balls])
            predict =predict[0]
            predict[0] =predict[0]*200
            predict[1] =predict[1]*420
            #print('predict ',predict)
        
        else:
            model_name = r"D:\MLGame-master\MLGame-master\MLP_model.sav"
            if os.path.isfile(model_name):
                f = open(model_name,'rb')
                MLP_model = pickle.load(f)
                
                tmp =[]
                l = len(self.ball_position)
                
                if l >0:
                    for i in range(0,50):
                        if len(self.ball_position)>i:
                            tmp.append(self.ball_position[l-i-1][0]/200)
                            tmp.append(self.ball_position[l-i-1][1]/420)
                        else:
                            tmp.append(0)
                            tmp.append(0)
                    
                   
                    balls = np.array(tmp)
                    predict = MLP_model.predict([balls])
                    predict =predict[0]
                    predict[0] =predict[0]*200
                    predict[1] =predict[1]*420
                else:
                    predict = [80,420]
                
            else:
                predict = [80,420]
        
        platform_position[0]=platform_position[0]+20
        if not self.ball_served:
            if self.side =='1P':
                if self.ball_position[-1][1]>=414:
                    predict[0] = 45
                    if platform_position[0] < predict[0]:
                        command = "MOVE_RIGHT"
                    elif platform_position[0] > predict[0]:
                        command = "MOVE_LEFT"
                    elif platform_position[0] == predict[0]:
                        self.ball_served = True
                        command = "SERVE_TO_LEFT"
                else:
                    self.ball_served = True
                    command = "NONE"
                    
            elif self.side =='2P':
                if self.ball_position[-1][1]<=81:
                    predict[0] = 45
                    if platform_position[0] < predict[0]:
                        command = "MOVE_RIGHT"
                    elif platform_position[0] > predict[0]:
                        command = "MOVE_LEFT"
                    elif platform_position[0] == predict[0]:
                        self.ball_served = True
                        command = "SERVE_TO_LEFT"
                else:
                    self.ball_served = True
                    command = "NONE"
            
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
    
    def test(self):
        ux = np.zeros(200)
        X_train =[]
        X_train.append(ux)
        X_train.append(ux)
        X_train.append(ux)
        
        X_train = np.array(X_train)
        #X_train = [[80,415,80,415,80,415,80,415],[80,415,80,415,80,415,80,415],[80,415,80,415,80,415,80,415]]
        y_train = [[20,120],[20,120],[20,120]]
        
        model_name = r"D:\MLGame-master\MLGame-master\MLP_model.sav"
        if os.path.isfile(model_name):
            f = open(model_name,'rb')
            MLP_model = pickle.load(f)
            MLP_model.fit(X_train, y_train)
            model_name_sav = "MLP_model.sav"
            pickle.dump(MLP_model, open(model_name_sav, 'wb'))
        else:
            MLP_model = MLPClassifier(hidden_layer_sizes=(50,), max_iter=10, alpha=1e-4,
                        solver='sgd', verbose=10, tol=1e-4, random_state=1,
                        learning_rate_init=.1)
            MLP_model.fit(X_train, y_train)
            model_name_sav = "MLP_model.sav"
            pickle.dump(MLP_model, open(model_name_sav, 'wb'))
            
        
       
        balls = np.array([(80,415),(80,415),(80,415),(80,415)])
        
        balls = balls.reshape(1, -1)
        predict = MLP_model.predict(balls)
        
    def test2():
        from sklearn.neighbors import KNeighborsClassifier 
        from sklearn.neural_network import MLPClassifier
        from sklearn.neural_network import MLPRegressor 
        import pickle
        import numpy as np
        import os
        import csv
        namex ='mlp_x_' + '2P' + 'logs.csv'
        namey ='mlp_y_' + '2P' + 'logs.csv'
        X_train =None
        y_train =None
        if os.path.isfile(namex) and os.path.isfile(namey):
            with open(namex, newline='') as csvfile:
                # 以冒號分隔欄位，讀取檔案內容
                rows = csv.reader(csvfile)
                X_train = np.array( rows)
            with open(namey, newline='') as csvfile:
                # 以冒號分隔欄位，讀取檔案內容
                rows = csv.reader(csvfile)
                y_train =np.array( rows)
        
        
        MLP_model =  MLPRegressor(solver='adam', alpha=1e-5, 
                                  hidden_layer_sizes=(100, ), random_state=1) 

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
        self.ball_position =[]
        self.end_position =[]
        self.starts_position =[]