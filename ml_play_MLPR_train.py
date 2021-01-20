# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 15:43:25 2021

@author: HQHQH
"""
import csv
import os
import math
import glob    
import numpy as np
import pickle
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

from os import listdir
from os.path import isfile, isdir, join

def getdis(center,end):
    disx =center[0] - end[0]
    disy =center[1] - end[1]
    powdis =(disx * disx) + (disy * disy)
    dis = math.sqrt(powdis)
    return dis


def getrangedis(dis):
    #maxdis =math.sqrt(200*200 +400*400)
    #maxdis = 447.21359549995793
    #range_th = 10 
    
    if len(dis)>1:
        dis_mean =np.mean(dis)
        dis_std =np.std(dis, ddof=1)
        if math.isnan(dis_std):
            dis_std =0
    else:
        if len(dis)==1:
            dis_mean =dis[0]
        else:
            dis_mean =0
        dis_std =0
    #normal_dis = [(d-dis_mean)/(3*dis_std) for d in dis ]
    
    # lens = 3
    # rang_rect = [0 for i in range(lens)]
    # for nd in normal_dis:
    #     index =math.ceil(nd*lens) 
    #     if index>=lens:
    #         index =lens-1
    #     elif index<=-lens:
    #         index =-lens+1
    #     rang_rect[index] +=1 
        
    rang_rect=[]
    rang_rect.append(round(dis_mean))
    rang_rect.append(round(dis_std*100))
    
    
    return rang_rect
def isdelgameoverfile():
    # 指定要列出所有檔案的目錄
    mypath = r'D:/MLGame-master/MLGame-master/games/pingpong/log'
    names=[]
    # 取得所有檔案與子目錄名稱
    files = listdir(mypath)
    total = len(files)
    print(total)
    indexs=[]
    for file in files:
        data_list = pickle.load(open(join(mypath, file),'rb'))
        # for index in  range(0, len(data_list['ml']['scene_info'])):
        #    if data_list['ml']['scene_info'][index]['status'] =='GAME_OVER':
        #        names.append(join(mypath, file))
        #        #print('del ',join(mypath, file))
        #        break
    
    if len(names)==0:
        print('no file need del')
    return names


def dataprocess(data_list):
    """
       Create a container to save the info from 'scene_info' dictionary
    """
    ball_position = []   # storage ball (x, y) position
    platform_1P_position = []   #storage platform (x,y) position
    platform_2P_position = []
    ball_status = []   #storage ball movement status{up, down, left, right}
    bricks_position =[]
    #hard_bricks_position=[]
    blockers_position = []
    commands=[]
    #ball_cross=[]
    goal_388=[]
    goal_395=[]
    vel = []
    status =[]
    """
       split the scene_info in several part, and put them into the container we
       create before (at top line)
    """
    tmpind=0
    
    ML = 'ml_1P'  #'ml_2P'
    
    for index in  range(0, len(data_list[ML]['scene_info'])):
        if data_list[ML]['scene_info'][index]['status'] =='GAME_OVER':
            return None,None
        # get the information of ball position from scene_info list
        ball_position.append(data_list[ML]['scene_info'][index]['ball'])
        # get the information of platform position frome scene_info list
        platform_1P_position.append(data_list[ML]['scene_info'][index]['platform_1P'])
        platform_2P_position.append(data_list[ML]['scene_info'][index]['platform_2P'])
        #ball_status.append(data_list['ml']['scene_info'][1][''])
        
        #and data_list[ML]['scene_info'][index]['ball_speed'][1]>0
        
        if data_list[ML]['scene_info'][index]['ball'][1]==415 :
           #[goal_388.append(data_list['ml']['scene_info'][index+1]['ball'][0]) for i in range(tmpind,index+1)]
           #[goal_395.append(data_list['ml']['scene_info'][index]['ball'][0]) for i in range(tmpind,index+1)]
           vel.append(data_list[ML]['scene_info'][index]['ball_speed'])
           goal_388.append(data_list[ML]['scene_info'][index+1]['ball'])
           goal_395.append(data_list[ML]['scene_info'][index]['ball'])
           if 'blocker' in data_list[ML]['scene_info'][index]:
               blockers_position.append(data_list[ML]['scene_info'][index]['blocker'])
           #hard_bricks_position.append(data_list['ml']['scene_info'][index]['hard_bricks'])
        
           tmpind = index+1
        
           
    
    for index in  range(0, len(data_list[ML]['command'])):
        commands.append(data_list[ML]['command'][index])
    
    ball_pos_array = np.array(ball_position) # convert to numpy type array
    platform_1P_pos_array = np.array(platform_1P_position) 
    platform_2P_pos_array = np.array(platform_2P_position) 
    blockers_pos_array = np.array(blockers_position) 
    #bricks_pos_array = np.array(bricks_position) 
    #hard_bricks_pos_array = np.array(hard_bricks_position)
    vel_array = np.array(vel) 
    goal_pos_388_array = np.array(goal_388) 
    goal_pos_395_array = np.array(goal_395) 
    nd_rects=[]
    command_labs=[]
    labs =["NONE","MOVE_RIGHT","MOVE_LEFT","SERVE_TO_RIGHT","SERVE_TO_LEFT"]
    
    eigen_vector =[]
    eigen_label =[]
    for i in range(2,len(goal_pos_395_array)):
        dis =[]
        # dis.append(getdis(ball_pos_array[i],[0,0]))
        # dis.append(getdis(ball_pos_array[i],[200,0]))
        # dis.append(getdis(ball_pos_array[i],[0,400]))
        # dis.append(getdis(ball_pos_array[i],[200,400]))
        # dis.append(getdis(ball_pos_array[i],[100,200]))
        #dis.append(getdis(ball_pos_array[i],platform_pos_array[i]))
        # for brick in bricks_pos_array[i-1]:
        #     dis.append(getdis(goal_pos_395_array[i-1],brick)) 
        # for hard_brick in hard_bricks_pos_array[i-1]:
        #     dis.append(getdis(goal_pos_395_array[i-1],hard_brick)) 
        # nd_rect = getrangedis(dis)
        
        # dis_n =[]
        # for brick in bricks_pos_array[i]:
        #     dis_n.append(getdis(goal_pos_395_array[i],brick)) 
        # for hard_brick in hard_bricks_pos_array[i]:
        #     dis_n.append(getdis(goal_pos_395_array[i],hard_brick)) 
        # nd_rect_n = getrangedis(dis_n)
        
        
        tmp =[]
        # tmp.extend(ball_pos_array[i-7])
        # tmp.extend(ball_pos_array[i-6])
        # tmp.extend(ball_pos_array[i-5])
        # tmp.extend(ball_pos_array[i-4])
        # tmp.extend(ball_pos_array[i-3])
        # tmp.extend(ball_pos_array[i-2])
        # tmp.extend(ball_pos_array[i-1])
        #tmp.extend(ball_pos_array[i])
        tmp.extend([goal_pos_395_array[i-1][0]])
        tmp.extend([vel_array[i-1][0]])
        if len(blockers_pos_array)>0:
            tmp.extend([blockers_pos_array[i-2][0]])
            tmp.extend([blockers_pos_array[i-1][0]])
        else:
            tmp.extend([-10])
            tmp.extend([-10])
        #tmp.extend(platform_pos_array[i])
        
        #tmp_n =[]
        # tmp_n.extend(ball_pos_array[i-3])
        # tmp_n.extend(ball_pos_array[i-2])
        # tmp_n.extend(ball_pos_array[i-1])
        # tmp_n.extend(ball_pos_array[i-0])
        # tmp_n.extend(ball_pos_array[i+1])
        # tmp_n.extend(ball_pos_array[i+2])
        # tmp_n.extend(ball_pos_array[i+3])
        #tmp_n.extend([goal_pos_395_array[i][0]])
        tmp_n=goal_pos_395_array[i][0]
        #tmp_n.extend(nd_rect_n)
        #tmp.extend(platform_pos_array[i])
        #nd_rect = tmp
        #nd_rects.append(tmp)
        
        # for lab in labs:
        #     if commands[i]==lab:
        #         command_labs.append(labs.index(lab))
        
        #command_labs =ball_pos_array[i]# goal_pos_array[8:]
        # lc =len(command_labs)
        # ln =len(nd_rects)
        # if lc<ln:
        #     eigen_vector.append(nd_rects[:lc])
        #     eigen_label.append( command_labs[:lc])
        # elif lc>ln:
        #     eigen_vector.append(nd_rects[:ln])
        #     eigen_label.append( command_labs[:ln])
        # else:
        eigen_vector.append(tmp)
        eigen_label.append( tmp_n)
            
    return eigen_vector,eigen_label
    
# Code bellow:

# pickle_file_path=r'D:/MLGame-master/MLGame-master/games/arkanoid/log/ml_NORMAL_1_2020-12-11_16-01-25.pickle'
# file_list = glob.glob(pickle_file_path)

# data_list = pickle.load(open(file_list[0],'rb'))



#%%
# 刪除失敗的紀錄
#names = isdelgameoverfile()
# 指定要列出所有檔案的目錄
mypath = r'D:/MLGame-master/MLGame-master/games/pingpong/log'

# 取得所有檔案與子目錄名稱
files = listdir(mypath)
knn_eigen_vector=[]
knn_eigen_label=[]

data_lists=[]
inedx=0
total = len(files)
print(total)
for file in files:
    if inedx<600:
        print('processing',inedx)
        data_list = pickle.load(open(join(mypath, file),'rb'))
        data_lists.append(data_list)
            
        eigen_vector,eigen_label = dataprocess(data_list)
        
        if eigen_vector==None:
            print('del ',join(mypath, file))
            os.remove(join(mypath, file))
        else:
            knn_eigen_vector.extend(eigen_vector)
            knn_eigen_label.extend(eigen_label)
            print('processed',inedx)
            inedx+=1
    else:
        break
knn_eigen_vector=np.array(knn_eigen_vector)
knn_eigen_label=np.array(knn_eigen_label)
    

#%%
# # 開啟輸出的 CSV 檔案
# data=[]
# with open('output.csv', 'w', newline='') as csvfile:
#     # 建立 CSV 檔寫入器
#     writer = csv.writer(csvfile)
    
#     # 寫入一列資料
#     writer.writerow(['序列', '輸入x','輸入y', '輸出'])
#     lens =len(knn_eigen_vector)
#     for i in range(lens):
#         data.append([knn_eigen_vector[i][0], knn_eigen_vector[i][1], knn_eigen_label[i]])
#         writer.writerow([i, knn_eigen_vector[i][0], knn_eigen_vector[i][1], knn_eigen_label[i]])
#%%
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
font = {'family' : 'SimHei',
'weight' : 'bold',
'size'  : '16'}
plt.rc('font', **font)        # 步驟一（設定字型的更多屬性）
plt.rc('axes', unicode_minus=False) # 步驟二（解決座標軸負數的負號顯示問題）
plt.rcParams['axes.facecolor'] = 'w'

x = [b[0] for b in knn_eigen_vector]
y = [b[1] for b in knn_eigen_vector]
z = [b[2] for b in knn_eigen_vector]
u = knn_eigen_label
#u2 = data_train.predict(knn_eigen_vector)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
#ax.scatter(x, y, np.zeros(len(x)),c='r', marker="*")
ax.scatter(x, y, u,c='r', marker="*")
#ax.scatter(y, u2, np.zeros(len(x)),c='g', marker="_")
# marker =[]
# colors =[]
# for n in u:
#     if n==0:
#         marker.append('o')
#         colors.append('g')
#     elif n==1:
#         marker.append(">")
#         colors.append('r')
#     elif n==2:
#         marker.append("<")
#         colors.append('b')
#     else:
#         marker.append('_')
#         colors.append('black')


#ax = fig.gca(projection='3d')

# for index in range(len(x)):
#     if colors[index] == 'g':
#         ax.scatter(x[index], y[index], u[index],c='g', marker='o')  #这里传入x, y, z的值
#     elif colors[index] == 'r':
#         ax.scatter(x[index], y[index], u[index],c='r', marker=">")  #这里传入x, y, z的值
#     elif colors[index] == 'b':
#         ax.scatter(x[index], y[index], u[index],c='b', marker="<")  #这里传入x, y, z的值
#     else:
#         ax.scatter(x[index], y[index], u[index],c='black', marker='_')  #这里传入x, y, z的值
ax.invert_yaxis()
ax.legend()

ax.set_xlabel('X 我方出發位置')
ax.set_ylabel('Y 出發的速度')
ax.set_zlabel('Z 回來的位置')
plt.show()

#%%
# from sklearn.preprocessing import PolynomialFeatures
# from sklearn.pipeline import make_pipeline
#from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor 
#model = LinearRegression(fit_intercept=True,normalize=True)
# model = make_pipeline(PolynomialFeatures(7), LinearRegression())
#model.fit(input_data, output_data)



#%%
# model =  MLPRegressor(solver='sgd',activation ='tanh', alpha=1e-6, 
#               hidden_layer_sizes=(120,32,4,4,32,16,8,120 ), random_state=0,max_iter=50000) 
# model =  MLPRegressor(solver='lbfgs',activation ='tanh', alpha=1e-8, 
#               hidden_layer_sizes=(128,32,4,4,32,16,8,128 ), random_state=0,max_iter=50000) 
#0.9998185711292447
input_data = knn_eigen_vector
output_data = knn_eigen_label


test =(16,128,128,16)
test2 =(16,128,128,16)

model =  MLPRegressor(solver='lbfgs',activation ='tanh', alpha=1e-5, verbose =True,
              hidden_layer_sizes=test, random_state=1,max_iter=50000)
model.fit(input_data, output_data)
r_squared = model.score(input_data, output_data)
print(r_squared)
model_name = "MLPR_1P.sav"
pickle.dump(model, open(model_name, 'wb'))


# model2 =  MLPRegressor(solver='lbfgs',activation ='tanh', alpha=1e-5, verbose =True,
#               hidden_layer_sizes=test2, random_state=1,max_iter=50000)
# model2.fit(input_data2, output_data2)
# r_squared2 = model2.score(input_data2, output_data2)
# print(r_squared2)
# model_name = "MLPR_2P.sav"
# pickle.dump(model, open(model_name, 'wb'))


filename = "D:\\MLGame-master\\MLGame-master\\games\\pingpong\\ml\\MLPR_1P.sav"
data_train = pickle.load(open(filename,'rb'))
# filename = "D:\\MLGame-master\\MLGame-master\\games\\pingpong\\ml\\MLPR_2P.sav"
# model2 = pickle.load(open(filename,'rb'))

#data_train

# #%%
# data_train = KNeighborsClassifier(n_neighbors=59)
# data_train.fit(knn_eigen_vector, knn_eigen_label)
# print(data_train.score(knn_eigen_vector, knn_eigen_label))
# #%%

# total =len(knn_eigen_label)
# tests=np.random.randint(total, size=10)#,
# for test in tests:
#     print (test,data_train.predict([knn_eigen_vector[test]])[0],knn_eigen_label[test])
# proba = data_train.predict_proba([knn_eigen_vector[15]])[0]
# print(len(proba))
# data_train.predict([knn_eigen_vector[test]])[0]
#%%
#model_name = "KNN_model.sav"
#pickle.dump(data_train, open(model_name, 'wb'))

#%%
error =[]
pre=[]
for index in range(len(x)):
    pre.append(data_train.predict([[x[index],y[index]]]))

for index in range(len(x)):
    error.append(abs(pre[index]-z[index]))
    
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for index in range(len(x)):
    if error[index] <10:
        ax.scatter(x[index], y[index], error[index],c='g', marker='o')  #这里传入x, y, z的值
    else:
        ax.scatter(x[index], y[index], error[index],c='r', marker='x')  #这里传入x, y, z的值
ax.legend()
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
plt.show()

model_name = "KNN_model.sav"
pickle.dump(data_train, open(model_name, 'wb'))
#%%

#樣本初始定義(X0:出發點,YL1,YR1,YL2,YR2) 預測 (左,中,右)
#                    得到Xb
