#!/usr/bin/env python
#coding = utf-8

import config
import dataspider
from database import CommentsDb
import time
import random
import dataaudit

# 得到歌曲列表
def get_songs(spider):
    songs = []  
    for album_id in spider.get_albums_id():
        for song_id in spider.get_songs_id(album_id[1]):
            songs.append(song_id)
    return songs


# 爬取歌曲评论并保存到数据库
def scrapyer(songs,spider,ComDb,total_com):
    wyycomments = ComDb.get_a_database('wyycomments')
    count = 1
    for song_name,song_id in songs: 
        collection = ComDb.get_a_collection(wyycomments,'{}-{}'.format(song_name,song_id))
        logs = ComDb.get_a_collection(wyycomments,'log')
        if ComDb.find_one(collection,{'_id':1}):
            continue # 若是一首歌已经爬取，则跳过该歌曲
        total = total_com['%s'%song_name] #得到一首歌曲评论总数
        print(total)
        limit = total/20 + 2  # 循环次数限制
        n = 0
        offset = 0
        little_scrapyer(count,n,limit,offset,spider,ComDb,collection,song_name,song_id,logs)

#供给scrapyer调用           
def little_scrapyer(count,n,limit,offset,spider,ComDb,collection,song_name,song_id,logs):
    while n < limit:#在此得到一首歌的评论并做存储
        time.sleep(random.randint(2,3))
        if count%1000 == 0:
            dataaudit.log('successfully get 1000 comments of {}'.format(song_name),logs)
        comments = spider.get_comments(song_id,offset)
        if comments['comments']==[]: #检查是否有评论数据
            print('empty comments')
        comments['_id'] = n  #指定文档id
        if ComDb.insert_one(collection,comments):
            print("successufully insert one doc in {}-{}".format(song_name,song_id),time.ctime(),'id:{}'.format(n))
            offset = offset + 20
            n = n + 1
            count = count + 1
        else: # 无法插入文档
            offset = offset + 20
            n = n + 1
            count = count + 1
            print("cant insert one doc in {}-{}".format(song_name,song_id),time.ctime(),'id:{}'.format(n))
            continue

# 重新爬取数据不完整的歌曲评论
def re_scrapyer(re_songs,spider,ComDb,total_com,count_indb):
    wyycomments = ComDb.get_a_database('wyycomments')
    logs = ComDb.get_a_collection(wyycomments,'log')
    count = 1
    for song_name,song_id in re_songs:
        collection = ComDb.get_a_collection(wyycomments,'{}'.format(song_name))
        total = total_com['%s'%song_name]
        limit = total/20 + 2  
        offset = count_indb['%s'%song_name]*20  # 从断点恢复减少重爬量
        n = count_indb['%s'%song_name]+1
        little_scrapyer(count,n,limit,offset,spider,ComDb,collection,song_name,song_id,logs)
            
if __name__ == "__main__":
    spider = dataspider.CommentsSpider(config.singer_id,'0') #得到一只爬虫对象
    ComDb = CommentsDb() #得到一个数据库对象
    #save_songs(songs,ComDb)
    #songs = dataaudit.songs_indb(ComDb)
    #total_com = dataaudit.total_indb(ComDb)
    #songs = [('遇见','287035')]
    total_com = {'遇见-287035':271327}
    #crapyer(songs,spider,ComDb,total_com)
    #re_songs = dataaudit.check_doc(songs,total_com,count_indb)
    #print(re_songs)
    #print(len(re_songs))
    re_songs = [('遇见-287035','287035')]
    count_indb = dataaudit.count_doc(re_songs,ComDb)
    re_scrapyer(re_songs,spider,ComDb,total_com,count_indb)

    

