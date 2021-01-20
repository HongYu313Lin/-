# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 00:58:24 2021

@author: HQHQH
"""
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np
import pickle
model = LinearRegression(fit_intercept=True)


rng = np.random.RandomState(1)
x = 10 * rng.rand(50)
y = 3 * x - 5 + rng.randn(50)
plt.scatter(x, y);
model.fit(x[:, np.newaxis], y)

xfit = np.linspace(0, 10, 1000)
yfit = model.predict(xfit[:, np.newaxis])

plt.scatter(x, y)
plt.plot(xfit, yfit)


#%%
def get_line_func(pos,vel):
    a = vel[1]/vel[0]
    b = pos[1]-a*pos[0]
    return a,b

def solve_x(line,y):
    x = (y-line[1])/line[0]
    return x

def limmit(posx,velx,maxx):
    q = abs(posx//(maxx))
    mod =abs( posx%(maxx))
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

def getl2(line,vel, y):
    x = solve_x(line, y)
    newx,newv = limmit( x, vel[0], 195)
    pos = [newx,y]
    vel = [newv,vel[1]]
    L2 =get_line_func(pos, vel)
    return L2

def ball_path_sim(pos,vel,y):
    L1 =get_line_func(pos, vel)
    #L1 =(L1[0],L1[1]/415)
    L2 = getl2( L1,vel,y)
    #L2 =(L2[0],L2[1])
    x = solve_x(L2, y)
    
    x = solve_x(L1, y)
    x,v=limmit(x,vel[0],196)
    return x,L2

#%%驗證
def valid(input_data,predict,y,vel=[0,0]):
    input_data=(input_data[0],input_data[1]*415)
    predict=(predict[0],predict[1]*415)
    ballline = input_data
    #vel =[7,7]
    preds=[]
    for i in range(415,80-1,-1):
        x = solve_x(ballline, i)
        newx,newv = limmit( x, vel[0], 195)
        pos = [newx,i]
        vel = [newv,vel[1]]
        preds.append(pos)
    preds =np.array(preds)
    DPI = plt.gcf().get_dpi()
    plt.gcf().set_size_inches(325.0/float(DPI),810.0/float(DPI))
    plt.gca().invert_yaxis()
    plt.plot(preds[:,0],preds[:,1])
    plt.text(preds[-1,0],preds[-1,1],str(preds[-1]),color='b',fontproperties='SimHei',fontsize='12',rotation=0)    
    plt.text(preds[0,0],preds[0,1],str(preds[0]),color='b',fontproperties='SimHei',fontsize='12',rotation=0)    
    
    x = solve_x(predict, y)
    print(x,y)
    plt.text(x,y+40,str([x,y]),color='r',fontproperties='SimHei',fontsize='12',rotation=0)  
#%%
#1p

vxs =[-7,7,10,-10]

y1 = 415

speed_1p =[-7,-7]
ball_1p =[0,y1]


poss =[]
speeds=[]
input_data = []
output_data = [] 
# 1   2   4  5   7  
#335 167 83 67  47

for py in range(80,415,67):
    for px in range(0,195+1):
        for vx in vxs:
            poss.append([px,py])
            speeds.append([vx,speed_1p[1]])
            
            L1 =get_line_func(poss[-1], speeds[-1])
            # L2 = getl2(L1,speeds[-1],80)
            L1 =(L1[0],L1[1]/415)
            # L2 =(L2[0],L2[1]/415)
            
            x,L2 = ball_path_sim(poss[-1], speeds[-1], 80)
            L2 =(L2[0],L2[1]/415)
            ball_2p = [x,80]
            srcspeed =abs(speeds[-1][0])
            if L2[0]>0:
                nspeed=speeds[-1]
            else:
                nspeed =[round(-(srcspeed)),-speeds[-1][1]]
                
            
            nx,nL2 = ball_path_sim(ball_2p, nspeed, 415)
            nL2 =(nL2[0],nL2[1]/415)
            
            LN =[L2[0],L2[1],nL2[0],nL2[1]]
            
            input_data.append(L1)
            output_data.append(LN)
            
index =107
tmp = [output_data[index][0],output_data[index][1]]
#tmpa = [output_data[index][0],output_data[index][1]]
tmp2 = [output_data[index][2],output_data[index][3]]
print(tmp,tmp2)
valid(input_data[index],tmp,80,[0,0])


valid(tmp2,tmp2,415,[0,0])


#%%
# 2p


vxs =[-7,7,10,-10]

y2 =80

speed_2p =[7,7]
ball_2p =[0,y2]

poss =[]
speeds=[]
input_data2 = []
output_data2 = [] 
for py in range(415,80,-67):
    for px in range(0,195+1):
        for vx in vxs:
            poss.append([px,py])
            speeds.append([vx,speed_2p[1]])
            
            L1 =get_line_func(poss[-1], speeds[-1])
            #L2 = getl2(L1,speeds[-1],415)
            L1 =(L1[0],L1[1]/415)
            #L2 =(L2[0],L2[1]/415)
            
            x,L2 = ball_path_sim(poss[-1], speeds[-1], 415)
            L2 =(L2[0],L2[1]/415)
            ball_2p = [x,415]
            srcspeed =abs(speeds[-1][0])
            if L2[0]>0:
                nspeed =[round(-(srcspeed)),-speeds[-1][1]]
            else:
                nspeed=speeds[-1]
            nx,nL2 = ball_path_sim(ball_2p, nspeed, 80)
            nL2 =(nL2[0],nL2[1]/415)
            
            LN =[L2[0],L2[1],nL2[0],nL2[1]]
            
            input_data2.append(L1)
            output_data2.append(LN)

index =82
tmp = [output_data2[index][0],output_data2[index][1]]
tmp2 = [output_data2[index][2],output_data2[index][3]]
print(tmp,tmp2)
valid(input_data2[index],tmp,415,[0,0])


valid(tmp2,tmp2,80,[0,0])


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


test =(16,128,128,16)
test2 =(16,128,128,16)

model =  MLPRegressor(solver='lbfgs',activation ='tanh', alpha=1e-5, verbose =True,
              hidden_layer_sizes=test, random_state=1,max_iter=50000)
model.fit(input_data, output_data)
r_squared = model.score(input_data, output_data)
print(r_squared)
model_name = "MLPR_1P.sav"
pickle.dump(model, open(model_name, 'wb'))


model2 =  MLPRegressor(solver='lbfgs',activation ='tanh', alpha=1e-5, verbose =True,
              hidden_layer_sizes=test2, random_state=1,max_iter=50000)
model2.fit(input_data2, output_data2)
r_squared2 = model2.score(input_data2, output_data2)
print(r_squared2)
model_name = "MLPR_2P.sav"
pickle.dump(model, open(model_name, 'wb'))


filename = "D:\\MLGame-master\\MLGame-master\\games\\pingpong\\ml\\MLPR_1P.sav"
model = pickle.load(open(filename,'rb'))
filename = "D:\\MLGame-master\\MLGame-master\\games\\pingpong\\ml\\MLPR_2P.sav"
model2 = pickle.load(open(filename,'rb'))

#%%
print(model.get_params())
print(model2.get_params())
#%%
index = 81
predict_datas = []

for i in range(0,200,50):
    index = i
    for data in input_data:
        predict_datas.append(model.predict([data])[0])
    predict_data = model.predict([input_data[index]])[0]
    print(predict_data ,output_data[index])
    valid(input_data[index],predict_data,80,[0,0])
    #valid(input_data[index],output_data[index],80,[0,0])

#plt.scatter(x, y)
plt.rcParams['axes.facecolor'] = 'w'
fig = plt.figure()
predict_datas =np.array(predict_datas)
input_data =np.array(input_data)
output_data =np.array(output_data)
ax = fig.add_subplot(221, projection='3d')
ax.scatter(input_data[:,0],input_data[:,1], output_data[:,0])
#ax.plot(input_data[:,0],input_data[:,1], output_data[:,0])
ax2 = fig.add_subplot(222, projection='3d')
ax2.scatter(input_data[:,0],input_data[:,1], output_data[:,1])
#ax2.plot(input_data[:,0],input_data[:,1], output_data[:,1])


ax3 = fig.add_subplot(223, projection='3d')
ax3.scatter(input_data[:,0],input_data[:,1], predict_datas[:3920,0])
#ax.plot(input_data[:,0],input_data[:,1], output_data[:,0])
ax4 = fig.add_subplot(224, projection='3d')
ax4.scatter(input_data[:,0],input_data[:,1], predict_datas[:3920,1])
#ax2.plot(input_data[:,0],input_data[:,1], output_data[:,1])



