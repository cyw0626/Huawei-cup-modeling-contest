import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#要求的数据
T=[0]*2000   #运行时间



#data为读入的数据
#获取数据
#加表头
data = pd.read_csv('D:/model/code/data/xxx2.csv')
data=np.array(data)
vLength=len(data[:,0])
bingo=np.zeros((2000,10000))
everyT=[0]*vLength

flag=1  #一个运动学片段里有多少个速度
index=temp=0     #生成数组序列标志
shortTime=1
shortTim=[]     #标志位判断短行程时间
shortDistance=data[:,0][0]
shortDis=[]    #标志位判断短行程距离 
for i in range(vLength):
    if(i>0):
        #加速度从当前时刻算
        accelerate=(data[:,0][i]-data[:,0][i-1])/3.6    #第i+1点的加速度
        if(accelerate!=0 and data[:,0][i]==0 and data[:,0][i+1]==0):            #停止点的判断条件,三个与操作
            # print('出现',accelerate,i)
            #停止点当前时刻a!=0,下一时刻v=0,表明下一时刻运动就结束了  
            #数据读入第index行
            # print(flag+1,temp)
            for j in range(flag-temp+2):
                #运动学片段
                bingo[index,:][j]=data[temp+j]
            shortTim.append(shortTime+1)
            shortDis.append(shortDistance)
            shortTime=0
            shortDistance=0
            #运行时间
            everyT[index]=i-temp
            #第几个片段
            index=index+1
            #起始点
            temp=flag+1
            flag=flag+1
        else:
            shortTime=shortTime+1
            shortDistance=shortDistance+data[:,0][i]
            flag=flag+1 
# print(index)
#短行程判断
short=0
for i in range(index):
    if(shortTim[i]<20 or shortDis[i]<10):
        short=short+1
        bingo=np.delete(bingo,i,axis=0) 
index=index-short

print('文件2生成运动片段个数：',index)           


#指标计算
#================
# 指标个数为index
#================
#要求的数据
Twait=[0]*index     #怠速
Tacc=[0]*index  #加速
Tdec=[0]*index  #减速
Tave=[0]*index #匀速
distance=[0]*index#路程
everyTemp=0
T=everyT[0:index]   #时间段
Speed=np.zeros((index,vLength))
sumaccSpeed=[0]*index   #平均加速度
sumdecSpeed=[0]*index   #平均减速度
accStd=[0]*index    #加速度标准差
speedStd=[0]*index  #速度标准差
aveSpeed=[0]*index  #平均速度
TwaitPercent=[0]*index  #怠速比例
TaccPercent=[0]*index   #加速比例
TdecPercent=[0]*index   #减速比例
TavePercent=[0]*index   #匀速比例

for i in range(index):    
    distance[i]=sum(bingo[i])
    timewait=1
    timeacc=1
    timeave=1
    timedec=1
    sumacc=1
    sumdec=1
    for j in range(T[i]):
        acc=(bingo[i][j]-bingo[i][j-1])/3.6
        Speed[i][j]=acc
        if (acc==0 and bingo[i][j]==0):
            timewait=timewait+1
        if (acc>0 and bingo[i][j]!=0):
            timeacc=timeacc+1
            sumacc=sumacc+acc
        if (acc<0 and bingo[i][j]!=0):
            timedec=timedec+1
            sumdec=sumdec+acc
        if (acc==0 and bingo[i][j]!=0):
            timeave=timeave+1    
    Twait[i]=timewait
    Tacc[i]=timeacc
    Tave[i]=timeave
    Tdec[i]=timedec
    sumaccSpeed[i]=sumacc/timeacc
    sumdecSpeed[i]=sumdec/timedec

maxSpeed=[0]*index
maxaccSpeed=[0]*index
mindecSpeed=[0]*index
for i in range(index):
    maxSpeed[i]=max(bingo[i,:])
    maxaccSpeed[i]=max(Speed[i,:])
    mindecSpeed[i]=min(Speed[i,:])
    accStd[i]=np.std(Speed[i,:][slice(T[i])],ddof=1)
    speedStd[i]=np.std(bingo[i,:][slice(T[i])],ddof=1)
    aveSpeed[i]=distance[i]/T[i]
    TwaitPercent[i]=Twait[i]/T[i]
    TaccPercent[i]=Tacc[i]/T[i]
    TdecPercent[i]=Tdec[i]/T[i]
    TavePercent[i]=Tave[i]/T[i] 

#矩阵的拼接
feature=np.vstack((TavePercent,TdecPercent,TaccPercent,T,distance,maxSpeed,aveSpeed,maxaccSpeed,mindecSpeed,sumaccSpeed,sumdecSpeed,speedStd,accStd,TwaitPercent))
feature2pca=np.transpose(feature)

# print('运行时间T：',T,'路程',distance,'最大速度：',maxSpeed,'平均速度：',aveSpeed,
#         '最大加速度：',maxaccSpeed,'最小减速度：',mindecSpeed,'平均加速度',sumaccSpeed,'平均减速度',sumdecSpeed,
#         '速度标准差：' ,speedStd,'加速度标准差：',accStd,
#         '怠速时间比例：',TwaitPercent,'加速时间比例：',TaccPercent,'减速时间比例：',TavePercent,'匀速时间比例：',TdecPercent)
# print('特征矩阵：',feature)

# 绘图
plt.plot(range(0,10000),bingo[100])
plt.show() 
np.savetxt('feature2pca.csv', feature2pca, delimiter = ',') 
#匀速时间比例，减速时间比例，怠速时间比例