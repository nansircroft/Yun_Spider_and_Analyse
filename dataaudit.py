#!/usr/bin/env python
#coding = utf-8

import config
import dataspider
from database import CommentsDb
import time
import random
import spidermain

#存储歌曲列表
def save_songs(songs,ComDb):
    wyycomments = ComDb.get_a_database('wyycomments')
    collection = ComDb.get_a_collection(wyycomments,'LIST OF SONG')
    logs = ComDb.get_a_collection(wyycomments,'log')
    songs = dict(songs)
    songs[r'遇见-287035']='287035'
    songs['_id']='LIST OF SONG'
    try:
        if ComDb.find_one(collection,{'_id':1}):
            return
        else:
            ComDb.insert_one(collection,songs)
            log('successfully save the list of song' ,logs)
            print('successfully save the list of song')
            return
    except Exception as e:
        print(e)

# 从数据库得到歌曲列表
def songs_indb(ComDb):
    wyycomments = ComDb.get_a_database('wyycomments')
    collection = ComDb.get_a_collection(wyycomments,'LIST OF SONG')
    songs_doc = ComDb.find_one(collection,{'_id':'LIST OF SONG'})
    songs = [(key,value) for key,value in songs_doc.items()]
    songs.pop(0)
    return songs

# 统计文档数量
def count_doc(ComDb):
    songs = songs_indb(ComDb)
    wyycomments = ComDb.get_a_database('wyycomments')
    total = 0
    count_indb = {}
    for song_name,song_id in songs:
        count = 0
        collection = ComDb.get_a_collection(wyycomments,'{}'.format(song_name))
        for flag in ComDb.find_many(collection):
            count+=1 if flag else count
            total+=1 if flag else total
        count_indb['%s'%song_name] = count
    count_indb['total']=total
    return count_indb

#得到每首歌的评论数量并做存储
def get_total(songs,ComDb,spider):
    wyycomments = ComDb.get_a_database('wyycomments')
    collection = ComDb.get_a_collection(wyycomments,'LIST OF SONG')
    total_com = {'_id':'COM NUM CHECK'}
    for song_name,song_id in songs:
        one = spider.get_comments(song_id,'0')
        total = one['total']
        total_com['%s'%song_name]= total
        print('successfully get total comments num of %s'%song_name,total) 
    ComDb.insert_one(collection,total_com)
    print('successfully insert the total num of all songs')
    return

# 从数据库得到每首歌的评论总数
def total_indb(ComDb):
    wyycomments = ComDb.get_a_database('wyycomments')
    collection = ComDb.get_a_collection(wyycomments,'LIST OF SONG')
    total_com = ComDb.find_one(collection,{'_id':'TOTAL CHECK'})
    return total_com

#检查文档完整性
def check_doc(songs,total_com,count_indb):
    not_cp = []
    for song_name,song_id in songs:
        error = total_com['%s'%song_name]/20 - count_indb['%s'%song_name]
        if error > 10: # 数据量误差超过大于10份文档则为不完整
            not_cp.append((song_name,song_id))
            print('%s is not complete with error %s'%(song_name,error))
    return not_cp
            

# 保存日志
def log(message,collection):
    try:
        collection.insert_one({'_id':'%s'%time.ctime(),'message':'%s'%message})
    except Exception:
        collection.insert_one({'_id':'%s'%time.ctime(),'message':'logging error'})
    return

# 删除空文档
def del_empty(ComDb):
    songs = songs_indb(ComDb)
    #songs = [('遇见-287035','287035')]
    wyycomments = ComDb.get_a_database('wyycomments')
    for song_name,song_id in songs:
        collection = ComDb.get_a_collection(wyycomments,'{}'.format(song_name))
        ComDb.del_many(collection,{'comments':[]})

# 删除欺骗文档
def del_cheating(ComDb):
    songs = songs_indb(ComDb)
    wyycomments = ComDb.get_a_database('wyycomments')
    for song_name,song_id in songs:
        collection = ComDb.get_a_collection(wyycomments,'{}'.format(song_name))
        ComDb.del_many(collection,{'code':-460})

#检查数据库完整性
def data_check(ComDb):
    songs = songs_indb(ComDb)
    count_indb = count_doc(ComDb)
    total_com = total_indb(ComDb)
    not_cp = check_doc(songs,total_com,count_indb)
    print(not_cp)
    print(len(not_cp))


if __name__ == "__main__":
    ComDb= CommentsDb()
    # spider = dataspider.CommentsSpider(config.singer_id,'0')
    #data_check(ComDb)
    #total_doc = total_indb(ComDb)
    # print(total_doc)
    #get_time(songs,ComDb)
    #songs = [('Leave','287546')]
    #del_empty(ComDb)
    # songs = spidermain.get_songs(spider)
    # save_songs(songs,ComDb)
    #del_cheating(ComDb)
    count = count_doc(ComDb)
    print(20*count['total'])