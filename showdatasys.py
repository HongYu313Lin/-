# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 14:03:27 2021

@author: HQHQH
"""
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time
import paho.mqtt.client as mqtt

# 當地端程式連線伺服器得到回應時，要做的動作
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # 將訂閱主題寫在on_connet中
    # 如果我們失去連線或重新連線時 
    # 地端程式將會重新訂閱
    client.subscribe("Try1P/MQTT")
    client.subscribe("Try2P/MQTT")

# 當接收到從伺服器發送的訊息時要進行的動作
def on_message(client, userdata, msg):
    # 轉換編碼utf-8才看得懂中文
    #print(msg.topic+" "+ msg.payload.decode('utf-8'))
    m_in=json.loads(msg.payload)
    #print(msg.topic+" "+str( m_in['frame']))
    
    # for ball in m_in['preballlog']:
    #     ax.scatter(ball[0], ball[1],c='g', marker='o') 
    pball =np.array( m_in['preball'])
    preballlogs=np.array(m_in['preballlog'])
    pca_ball =np.array( m_in['precutaddball'])
    pca_balllogs=np.array(m_in['precutaddballlog'])
    pci_ball =np.array( m_in['precutinvball'])
    pci_balllogs=np.array(m_in['precutinvballlog'])
    
    
    ball =np.array( m_in['ball'])
    
    pbricks =np.array( m_in['prebrickslog'])
    #print(msg.topic+" "+str( preballlogs[:,0]))
    # lines = ax.plot(0, 0)[0] 
    # lines2 = ax2.plot(0, 0)[0] 
    if m_in['side'] == '1P':
        
        #預測球路徑  不切球
        lines.set_color("red")
        lines.set_xdata(preballlogs[:,0])
        lines.set_ydata(preballlogs[:,1])
        
        #預測球路徑  切快球
        print(str(pca_balllogs))
        ca_lines.set_color("green")
        ca_lines.set_xdata(pca_balllogs[:,0])
        ca_lines.set_ydata(pca_balllogs[:,1])
        
        #預測球路徑  切反球
        ci_lines.set_color("white")
        ci_lines.set_xdata(pci_balllogs[:,0])
        ci_lines.set_ydata(pci_balllogs[:,1])
        
        #預測球的落點  不切球
        psct.set_xdata(pball[0])
        psct.set_ydata(pball[1])
        
        #預測球的落點  切快球
        ca_psct.set_xdata(pca_ball[0])
        ca_psct.set_ydata(pca_ball[1])
        
        #預測球的落點  切反球
        ci_psct.set_xdata(pci_ball[0])
        ci_psct.set_ydata(pci_ball[1])
        
    elif m_in['side'] == '2P':
        
        #預測球路徑  不切球
        lines2.set_color("blue")
        lines2.set_xdata(preballlogs[:,0])
        lines2.set_ydata(preballlogs[:,1])
        
        #預測球路徑  切快球
        ca_lines2.set_color("green")
        ca_lines2.set_xdata(pca_balllogs[:,0])
        ca_lines2.set_ydata(pca_balllogs[:,1])
        
        #預測球路徑  切反球
        ci_lines2.set_color("white")
        ci_lines2.set_xdata(pci_balllogs[:,0])
        ci_lines2.set_ydata(pci_balllogs[:,1])
        
        #預測球的落點  不切球
        psct2.set_xdata(pball[0])
        psct2.set_ydata(pball[1])
        
        #預測球的落點  切快球
        ca_psct2.set_xdata(pca_ball[0])
        ca_psct2.set_ydata(pca_ball[1])
        
        #預測球的落點  切反球
        ci_psct2.set_xdata(pci_ball[0])
        ci_psct2.set_ydata(pci_ball[1])
    
    #print(str(pbricks))
    
    
    #球現在的位置
    sct.set_xdata(ball[0])
    sct.set_ydata(ball[1])
    
    sct2.set_xdata(ball[0])
    sct2.set_ydata(ball[1])
    
    
    for i in range(len(rects)):
        if i< len(pbricks):
            rects[i].set_xy(pbricks[i])
            rect2s[i].set_xy(pbricks[i])
        else:
            rects[i].set_xy((-100,-100))
            rect2s[i].set_xy((-100,-100))
            
    
    fig.canvas.draw()
    fig.canvas.flush_events()
    #time.sleep(0.5)
    
plt.rcParams['axes.facecolor'] = 'black'
x = np.linspace(0, 200, 20)
y = np.linspace(0, 500, 20)
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

ax.invert_yaxis()
ax2.invert_yaxis()

lines = ax.plot(x, y)[0] 
lines2 = ax2.plot(x, y)[0]

ca_lines = ax.plot(x, y,linewidth=1.5,linestyle="-.")[0] 
ca_lines2 = ax2.plot(x, y,linewidth=1.5,linestyle="-.")[0]

ci_lines = ax.plot(x, y,linewidth=0.5,linestyle="--")[0] 
ci_lines2 = ax2.plot(x, y,linewidth=0.5,linestyle="--")[0]

rects =[]
rect2s =[]
for i in range(10):
    color = (0.8+i*0.02,0.8-i*0.08,0.)
    rects.append(ax.add_patch(
     patches.Rectangle(
        (1, 1),
        35,
        25,
        edgecolor = color,
        facecolor = 'w',
        fill=False      
     ) ))
    rect2s.append(ax2.add_patch(
     patches.Rectangle(
        (1, 1),
        35,
        25,
        edgecolor = color,
        facecolor = 'w',
        fill=False      
     ) ))

 
sct = ax.plot(0, 0,'o',markersize=6,color=(0.,0.8,0.),markerfacecolor='none')[0] 
sct2 = ax2.plot(0, 0,'o',markersize=6,color=(0.,0.8,0.),markerfacecolor='none')[0] 

psct = ax.plot(0, 0,'o',markersize=6,color="red",markerfacecolor='none')[0] 
psct2 = ax2.plot(0, 0,'o',markersize=6,color="blue",markerfacecolor='none')[0] 

ca_psct = ax.plot(0, 0,'o',markersize=8,color=(0.,1.,0.),markerfacecolor='none')[0] 
ca_psct2 = ax2.plot(0, 0,'o',markersize=8,color=(0.,1.,0.),markerfacecolor='none')[0] 

ci_psct = ax.plot(0, 0,'o',markersize=6,color=(1.,1.,1.),markerfacecolor='none')[0] 
ci_psct2 = ax2.plot(0, 0,'o',markersize=6,color=(1.,1.,1.),markerfacecolor='none')[0] 

#plt.xlabel('X Label')
#plt.ylabel('Y Label')

# 連線設定
# 初始化地端程式
client = mqtt.Client()

# 設定連線的動作
client.on_connect = on_connect

# 設定接收訊息的動作
client.on_message = on_message

# 設定登入帳號密碼
client.username_pw_set("try","1234")

# 設定連線資訊(IP, Port, 連線時間)
client.connect("localhost", 1883, 60)

# 開始連線，執行設定的動作和處理重新連線問題
# 也可以手動使用其他loop函式來進行連接
client.loop_forever()
        
