import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
#import wordcloud
import jieba
import jieba.analyse
from matplotlib import image
import os
def bar_chart(dataset):
    x = np.unique(dataset.day.values)
    y = {}
    for d in x:
        y[d]=0
    for d in dataset.day.values:
        y[d]+=1
    y = np.array(list(y.values()))
    sns.set(color_codes=True)
    plt.figure(figsize=[10,12],dpi=120)
    plt.ylabel('comments number/item')
    plt.xlabel('time/day')
    plt.title('《遇见》2019年11月日评论数量')
    plt.plot(x, y) #绘制折线图
    plt.rcParams['font.sans-serif']=['simhei'] #设置字体
    for x1, y1 in zip(x, y):
        plt.text(x1 , y1, '%d' % (y1 ))#x1,y1坐标
    plt.show()
if __name__ == "__main__":
    dataset = pd.read_csv('D:/tx/data/normal/遇见-287035-287035.csv')
    #bar_chart(dataset)
    #word_cloud(dataset)
    bar_chart(dataset)