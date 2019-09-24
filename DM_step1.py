import xlrd   
import xlwt 
import numpy as np                                                    #导入xlrd模块
import time
file_name = "text2.xlsx"
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
K=145827#K=185726
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
over_data=0
error=0
start_data=0
start_delet_order=[0]*(712)
sdo=0
over_delet_order=[0]*(712)
odo=0
count=1
time_error=0
new_time_error=0
baderror=0
h=0
time_error=np.zeros((712))
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
                            time_error[h]=(day[i+1]*86400+hour[i+1]*3600+mins[i+1]*60+sec[i+1])-(day[i]*86400+hour[i]*3600+mins[i]*60+sec[i])
                            #new_time_error=time_error+new_time_error
                            if time_error[h]>60:
                                #new_time_error=time_error+new_time_error
                                for k in range(i,0,-1):
                                    #start_time_delet_order[sd0]=k
                                    if ex_speed[k]<=10:
                                        start_data=ex_data[k]
                                        start_delet_order[sdo]=k
                                        sdo+=1
                                        print ('start_data=',start_data)
                                        #print ('start_delet_order=',start_delet_order)
                                        break
                                for k in range (i+1,len(ex_data)):
                                    if ex_speed[k]<=10:
                                        over_data=ex_data[k]
                                        over_delet_order[odo]=k
                                        odo+=1
                                        print ('over_data=',over_data)
                                        #print ('over_delet_order=',over_delet_order)
                                        break
                            h+=1

                            #time_error=0
                                #error=over_delet_order-start_delet_order
                                #print ('error=',error)
                            #print ('temp_ex_data=',temp_ex_data)
                                #print ('len(ex_data)=',len(ex_data))
                                
                            #count=0
#print ('start_delet_order=',start_delet_order)
#print ('len_start_delet_order=',len(start_delet_order))
#print ('over_delet_order=',over_delet_order)

#print ('new_time_error=',new_time_error)
print ('len_over_delet_order=',len(over_delet_order))
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

#np.savetxt('data_2.csv', ex_data, fmt='%s') 
#np.savetxt(‘foo.csv’,uni,delimiter=’,’ fmt = ‘%s’)   
#np.savetxt('speed_2.csv', ex_speed, delimiter = ',')  