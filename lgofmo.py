import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import LinearLocator
from mlxtend.regressor import LinearRegression
import datetime
import time

rowdata = pd.read_csv('data/normal/祝你开心-287277.csv')
year = rowdata.year
month = rowdata.month

date = {}
for i in range(len(year)):
    da = f'{year[i]}-{month[i]}'
    if da not in date.keys():
        date[da]=1
    else:
        date[da]+=1

points = [(key,value) for key,value in date.items()][::-1]
gd_lr = LinearRegression()
x_ = [float(time.mktime(time.strptime(x[0], "%Y-%m"))) for x in points]
y_ = [float(y[1]) for y in points]
gd_lr.fit(np.array(x_)[:, np.newaxis],np.array(y_))
x_axis = [time.strftime("%Y-%m",time.localtime(i)) for i in x_]

print(x_axis[::18])
plt.rcParams['font.sans-serif']=['simhei'] #设置字体
plt.figure(figsize=[12,8])
plt.title('孙燕姿《祝你开心》月均评论数量回归模型')
plt.scatter(x_axis, y_,alpha=0.8,edgecolors= 'white')
plt.xlabel("日期")
plt.ylabel("评论数")
#plt.xticks(range(7), [2013,2014,2015,2016,2017,2018,2019])
#plt.yticks(y_, fontsize=9)
plt.plot(x_axis, gd_lr.predict(np.array(x_)[:, np.newaxis]), color='red')
ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
xmajorLocator  = LinearLocator(10)
ax.xaxis.set_major_locator(xmajorLocator)
plt.savefig('./picture/analyse/孙燕姿《祝你开心》月均评论数量回归模型.png')
plt.show()