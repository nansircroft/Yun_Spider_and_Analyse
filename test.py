# #获取属性
# html = '''
# <div class="wrap">
#    <div id="container">
#        <ul class="list">
#            <li class="item-0">first item</li>
#            <li class="item-1"><a href="link2.html">second item</a></li>
#            <li class="item-0 active"><a href="link3.html"><span class="boid">third item</span></a></li>
#            <li class="item-1 active"><a href="link4.html">fourth item</a></li>
#            <li class="item-0"><a href="link5.html">fifth item</a></li>
#        </ul>
#    </div>
# </div>
# '''

# from pyquery import PyQuery as pq

# doc = pq(html)

# a = doc(".item-0.active a")#选择class同时为item-0和active，在选择class里面的啊标签，中间注意空格

# print(a)

# print(a.attr("href"))

# print(a.attr.href)#结果同上

# #获取文本

# print(a.text())#将上面的选中的class中包围的文字

# #获取HTML

# a1 = doc(".item-0.active")

# print(a1.html())

# str='hello world'

# str0='''155226514651'''

# print(type(str),type(str0))

# class TestA(object):     
#     e = 2     
#     def __init__(self):        
#         self.a = 10       
#         self.b = 5        
#         c = 3  
#         print(c)

#     def pp(self):
#         c =0
#         print(c)


# # if __name__ == '__main__':    
# #     test_a = TestA()    
# #     print(test_a.a)    
# #     print(test_a.b)    
# #     print(test_a.e)    
# #     print(test_a.pp)  # 错误的写法

# def gen():
#     yield 1

# print(type(gen))
# print(type(gen()))

# print(gen().__next__())
# print(gen().__next__())

# gen = gen()
# print(gen.__next__())
# print(gen.__next__())
# import requests
# from pyquery import PyQuery as pq
# import config
# import re
# if __name__ == "__main__":
#     url = 'https://music.163.com/#/song?id=1379481976'
#     res = requests.get(url,headers=config.headers)
#     # with open('songtest.html','w') as f:
#     #     f.write(res.text)
#     # print(res.text)
#     # html = pq(res.text)
#     # total = html('#auto-id-yNHX8bbG85GFEMEB')
#     pattern = re.compile(r'<span class="sub s-fc3">共<span class="j-flag">(.*)</span>条评论</span>')
#     for i in re.findall(pattern,res.text):
#         print(i)

# import dataspider
# import config
# import dataaudit
# import spidermain
# from database import CommentsDb
# spider = dataspider.CommentsSpider(config.singer_id,'0')
# songs = spidermain.get_songs(spider)
# print(songs)
# for s in songs:
#     if s[0]=='遇见':
#         print(s)

# albums = [album for album in spider.get_albums_id()]
# print(albums)
# print(len(albums))
# for a in albums:
#     if a[0] == '经典全纪录(主打精华版)':
#         print(a)
# page = spider._CommentsSpider__get_album_page('28542')
# with open('star.html','w',encoding = 'utf-8') as f:
#     f.write(page)
# # count = 0
# for key,value in songs.items():
#     if key == '遇见':
#         print(value)
# com = spider.get_comments('287035','0')
# print(com['total'])
# comdb = CommentsDb()
# songs = dataaudit.songs_indb(comdb)
# total = {}
# for song_name,song_id in songs:
#     c = spider.get_comments(song_id,'0')
#     total['%s'%song_name]=c['total']

# print(total['遇见'])

# print(dict(songs)['遇见'])
import pandas as pd

file = pd.read_csv('./data/normal/遇见-287035-287035.csv')

print(file.tail())