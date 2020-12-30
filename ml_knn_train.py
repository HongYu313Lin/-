# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 17:55:58 2020

@author: HQHQH
"""
# import library:
import csv


import glob    
import numpy as np
import pickle
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

# Code bellow:

pickle_file_path=r'D:/MLGame-master/MLGame-master/games/arkanoid/log/ml_NORMAL_1_2020-12-11_16-01-25.pickle'
file_list = glob.glob(pickle_file_path)

data_list = pickle.load(open(file_list[0],'rb'))


"""
   Create a container to save the info from 'scene_info' dictionary
"""

ball_position = []   # storage ball (x, y) position
platform_position = []   #storage platform (x,y) position
ball_status = []   #storage ball movement status{up, down, left, right}



"""
   split the scene_info in several part, and put them into the container we
   create before (at top line)
"""

for index in  range(0, len(data_list['ml']['scene_info'])):
   
   # get the information of ball position from scene_info list
   ball_position.append(data_list['ml']['scene_info'][index]['ball'])
   # get the information of platform position frome scene_info list
   platform_position.append(data_list['ml']['scene_info'][index]['platform'])
   #ball_status.append(data_list['ml']['scene_info'][1][''])


ball_pos_array = np.array(ball_position) # convert to numpy type array
platform_pos_array = np.array(platform_position) # convert to numpy type array
platform_x_pos_array = np.array(platform_pos_array[:,0]) # capture x position from platform

# Combine the vector you create above that you would like to train later 
knn_eigen_vector = ball_pos_array
knn_eigen_label = platform_x_pos_array



# 開啟輸出的 CSV 檔案
data=[]
with open('output.csv', 'w', newline='') as csvfile:
    # 建立 CSV 檔寫入器
    writer = csv.writer(csvfile)
    
    # 寫入一列資料
    writer.writerow(['序列', '輸入x','輸入y', '輸出'])
    lens =len(knn_eigen_vector)
    for i in range(lens):
        data.append([knn_eigen_vector[i][0], knn_eigen_vector[i][1], knn_eigen_label[i]])
        writer.writerow([i, knn_eigen_vector[i][0], knn_eigen_vector[i][1], knn_eigen_label[i]])

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
 
x = [b[0] for b in data]
y = [b[1] for b in data]
z = [b[2] for b in data]
u = [x[i] - z[i] for i in range(len(x))]
marker =[]
colors =[]
for n in u:
    if n<10:
        marker.append('o')
        colors.append('g')
    else:
        marker.append('x')
        colors.append('r')

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
#ax = fig.gca(projection='3d')

for index in range(len(x)):
    if colors[index] == 'r':
        ax.scatter(x[index], y[index], z[index],c='g', marker='o')  #这里传入x, y, z的值
    else:
        ax.scatter(x[index], y[index], z[index],c='r', marker='x')  #这里传入x, y, z的值
ax.legend()
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
plt.show()

data_train = KNeighborsClassifier()
data_train.fit(knn_eigen_vector, knn_eigen_label)


print (data_train.predict([[74,33]]))

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



