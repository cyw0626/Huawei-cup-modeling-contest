
#-*-coding:utf-8-*-
import numpy as np
import pandas as pd
from scipy import linalg,stats
import matplotlib.pyplot as plt
import seaborn as sns
#sns.set()
from matplotlib.font_manager import FontProperties
from pylab import *
#fname = "/home/w/soft/anaconda2/envs/lstm/lib/python3.6/site-packages/matplotlib/mpl-data/fonts/ttf/SimHei.ttf"
#myfont = FontProperties(fname=fname)

#data = pd.read_csv('file1.csv')

def pca():
    Xtrain= pd.read_csv('feature2pca.csv')
    # Xtest = xx_test
    #print('Xtrain=',Xtrain)
    #print('Xtrain.shape=',Xtrain.shape)
    # 标准化处理
    X_mean = np.mean(Xtrain, axis=0)  #按求Xtrain平均值
    X_std = np.std(Xtrain, axis=0)  #求标准差
    #print('X_std=',X_std)
    X_row,X_col = Xtrain.shape  #求Xtrain行、列数
    Xtrain = (Xtrain-np.tile(X_mean,(X_row,1)))/np.tile(X_std,(X_row,1))##将平均值扩展为与xtrain相同形状的，横向拉伸
   # print('Xtrain=',Xtrain)
    # 求协方差矩阵
    sigmaXtrain = np.cov(Xtrain, rowvar=False)#rowvar=0，说明传入的数据一列代表一个变量，一行代表一个样本
    #对协方差矩阵进行特征分解，lamda为特征值构成的，T的列为单位特征向量，且与lamda中的特征值一一对应：
    lamda,T = linalg.eig(sigmaXtrain)
    
    #取对角元素(结果为一列向量)，即lamda值，并上下反转使其从大到小排列，主元个数初值为1，若累计贡献率小于90%则增加主元个数
    # D = flipud(diag(lamda))
    T = T[:,lamda.argsort()]  #将T的列按照lamda升序排列，从小到大，返回的是索引值

    print ('lamda.argsort()=',lamda.argsort())
    lamda.sort()  #将lamda按升序排列
    D = -np.sort(-np.real(lamda))  #提取实数部分，按降序排列
    num_pc = 1
    if (sum(D[0:num_pc])/sum(D))<0.85:
        num_pc += 1
    num_pc+=1
   
    #取与lamda相对应的特征向量
    P = T[:,X_col-num_pc:X_col]
  #print ('主元的特征向量',P)
   # print ('主元的特征向量shape',P)
    print('主元个数＝',num_pc)
    gong=D[0:X_col+1]/sum(D)
    fig,axes=plt.subplots(2,1)
    data=pd.Series(gong,index=list('1234567689abcd'))
    data.plot.barh(ax=axes[1],color='blue',alpha=0.7)
    data.plot.bar(ax=axes[0],color='blue',alpha=0.7,rot=0)
    fig.savefig('p2.png')
 #   print('第一个主元是'，lamda.argsort(１))
    Z=np.dot(Xtrain,P)
    print('贡献率：',gong)
    print('得分：',Z[0:6])
    pass




if __name__=='__main__':
    # data()
    pca()
