# !usr/bin/env python
# -*-coding:utf-8 -*-

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import wordcloud
import jieba
import jieba.analyse
from matplotlib import image
import os

#日均评论数量散点图
def bubble_chart(dataset):
    x = np.unique(dataset.day.values)
    y = {}
    for d in x:
        y[d]=0
    for d in dataset.day.values:
        y[d]+=1
    y = np.array(list(y.values()))
    plt.figure()
    plt.scatter(x,y)
    plt.show()

#日评论数量柱状图
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
    plt.xlabel('date/day')
    plt.title('《遇见》2019年11月日评论数量')
    plt.bar(x, y, width=0.8,color="#87CEFA") #绘制柱状图
    plt.rcParams['font.sans-serif']=['simhei'] #设置字体
    for x, y in zip(x, y):
        plt.text(x + 0.05, y + 0.1, '%d' % y, ha = 'center', va = 'bottom')
    #plt.savefig('./picture/analyse/遇见2019年11月日评论数量柱状图.png')
    plt.show()

#月评论数量柱状图
def bar_year(dataset):
    x = np.unique(dataset.year.values)
    y = {}
    for d in x:
        y[d]=0
    for d in dataset.year.values:
        y[d]+=1
    y = np.array(list(y.values()))
    sns.set(color_codes=True)
    plt.figure(figsize=[10,12],dpi=120)
    plt.ylabel('comments number/item')
    plt.xlabel('date/year')
    plt.title('《不能和你一起》年均评论数量柱状图')
    plt.bar(x, y, width=0.8,color="#87CEFA") #绘制柱状图
    plt.rcParams['font.sans-serif']=['simhei'] #设置字体
    for x, y in zip(x, y):
        plt.text(x + 0.05, y + 0.1, '%d' % y, ha = 'center', va = 'bottom')
    #plt.savefig('./picture/analyse/不能和你一起年均评论数量柱状图.png')
    plt.show()

#词云
def word_cloud(dataset):
    comments = dataset.content.values
    key_words = []
    for text in comments:
        k =jieba.analyse.extract_tags(text, topK=5, withWeight=False, allowPOS=())
        for kk in k:
            key_words.append(kk)
    key_words = ' '.join(key_words)
    bg_pic = image.imread('./picture/zz.jpg')
    wc = wordcloud.WordCloud(
        mask=bg_pic,
        background_color='white',
        font_path=r'C:\Windows\Fonts\simhei.ttf',
        ).generate(key_words)
    plt.figure(figsize=[10,8],dpi=120)
    plt.imshow(wc)
    plt.axis("off")
    wc.to_file("./picture/analyse/雨还是不停地落下.png") #保存
    plt.show()

if __name__ == "__main__": 
    dataset = pd.read_csv('./data/normal/不能和你一起-287325.csv')
    #bar_chart(dataset)
    #word_cloud(dataset)
    bar_year(dataset)