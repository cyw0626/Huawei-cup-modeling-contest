import xlrd   
import xlwt 
import numpy as np                                                    #导入xlrd模块
import time
def init_data(file_name,K):
    #file_name = "text1.xlsx"
    file = xlrd.open_workbook(file_name)
    
    # 输出Excel中表的个数
    #print(file.nsheets)
    
    # 读取某张表
    sheet = file.sheet_by_name("sheet1")
    # 获取表的行数
    nrows = sheet.nrows
    # 获取表的列数
    ncols = sheet.ncols
    #print("nrows: %d, ncols: %d" % (nrows, ncols))
    str_data = sheet.col_values(0)
    str_speed = sheet.col_values(1)
    # 获取第一行第一列的数据
    ex_data=[0]*(nrows+2)
    ex_speed=[0]*(nrows+2)
    #K=185726#K=185726
    year=np.zeros((K,1))
    mon=np.zeros((K,1))
    day=np.zeros((K,1))
    hour=np.zeros((K,1))
    mins=np.zeros((K,1))
    sec=np.zeros((K,1))
    for x in range(1,len(str_speed)-nrows+K):
        ex_speed[x]=str_speed[x]
        
    for x in range(1,len(str_data)-nrows+K):
        ex_data[x]=str_data[x]
        ex_data[x]=ex_data[x][0:19]
        #temp_ex_data[x]=ex_data[x]
        i = time.strptime(ex_data[x], '%Y/%m/%d %H:%M:%S')
        year[x-1]=np.array(i.tm_year)
        mon[x-1]=np.array(i.tm_mon)
        day[x-1]=np.array(i.tm_mday)
        hour[x-1]=np.array(i.tm_hour)
        mins[x-1]=np.array(i.tm_min)
        sec[x-1]=np.array(i.tm_sec)
    return ex_speed,ex_data,year,mon,day,hour,mins,sec
def ex_infor(ex_speed,ex_data,year,mon,day,hour,mins,sec,K):
    over_data=0
    start_data=0
    start_delet_order=[0]*(3000)
    sdo=0
    over_delet_order=[0]*(3000)
    odo=0
    count=1
    baderror=0
    for i in range(K):
        if i<K-1:
            if  sec[i+1]-sec[i]==1:
                count+=1
            else:
                if sec[i+1]-sec[i]==-59 and mins[i+1]-mins[i]==1:
                    count+=1
                else:
                    if mins[i+1]-mins[i]==-59 and hour[i+1]-hour[i]==1:
                        count+=1
                    else:
                        if hour[i+1]-hour[i]==-23 and day[i+1]-day[i]==1:
                            count+=1
                        else:
                            if day[i+1]-day[i]==-31 or day[i+1]-day[i]==-30 and mon[i+1]-mon[i]==1:
                                count+=1
                            else:
                                print('连续时间数＝',count)
                                baderror+=1
                                print('断点总数＝',baderror)
                                #print('断点开始点＝',ex_data[i+1])
                                #print('断点结束点＝',ex_data[i+2])
                                if day[i+1]-day[i]<=1 and mins[i+1]-mins[i]!=1:
                                    for k in range(i,0,-1):
                                        if ex_speed[k]>=10:
                                            start_data=ex_data[k]
                                            start_delet_order[sdo]=k
                                            sdo+=1
                                            print ('start_data=',start_data)
                                            #print ('start_delet_order=',start_delet_order)
                                            break
                                    for k in range (i+1,len(ex_data)):
                                        if ex_speed[k]>=10:
                                            over_data=ex_data[k]
                                            over_delet_order[odo]=k
                                            odo+=1
                                            print ('over_data=',over_data)
                                            #print ('over_delet_order=',over_delet_order)
                                            break
    return start_delet_order,over_delet_order
def infor_delet(start_delet_order,over_delet_order,ex_data,ex_speed):
    ee=0
    ee_sum=0
    for i in range (len(over_delet_order)):
        ee=over_delet_order[i]-start_delet_order[i]
        ee_sum=ee_sum+ee
        for j in range(len(over_delet_order)):
            over_delet_order[j]=over_delet_order[j]-ee
            start_delet_order[j]=start_delet_order[j]-ee
        for j in range (start_delet_order[i]-1,start_delet_order[i]+1):
            if j==start_delet_order[i]:
                for k in range(1,ee+1):
                    ex_data=np.delete(ex_data,j+k,0)
                    ex_speed=np.delete(ex_speed,j+k,0)
        #print ('ex_data=',len(ex_data))
    print ('new_ex_data=',len(ex_data))
    print ('ee_sum=',ee_sum)
    print ('ex_data=',ex_data)
    print ('ex_speed=',ex_speed.shape)
    return ex_data,ex_speed
file_name = "text3.xlsx"
K=164915#K=185726#K=145826
ex_speed,ex_data,year,mon,day,hour,mins,sec=init_data(file_name,K)
start_delet_order,over_delet_order=ex_infor(ex_speed,ex_data,year,mon,day,hour,mins,sec,K)
#del_data,del_speed=infor_delet(start_delet_order,over_delet_order,ex_data,ex_speed)
#np.savetxt('data.csv', del_data, fmt='%s') 
#np.savetxt('speed.csv', del_speed, delimiter = ',')  

