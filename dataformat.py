#!usr/bin/env python
#coding = utf-8

import config
from database import CommentsDb
import time
import random
import spidermain
import dataaudit
import csv
import dataspider
#得到每条评论的评论时间、内容、点赞数、用户名、用户id
def get_fromat(songs,ComDb,c):
    wyycomments = ComDb.get_a_database('wyycomments')
    formated_data = {}
    for song_name,song_id in songs:
        collection = ComDb.get_a_collection(wyycomments,'{}'.format(song_name))
        per_song = []
        count = 0
        for doc in ComDb.find_many(collection):
            try:
                comm = doc['%s'%c]
                if comm == []:
                    spider = dataspider.CommentsSpider(config.singer_id,'0')
                    one =spider.get_comments(song_id,'0')
                    comm = one['hotComments']
                    print(comm)
                for row in comm:
                    count += 1
                    year = int(time.strftime('%Y',time.localtime(int(row['time'])/1000)))
                    month = int(time.strftime('%m',time.localtime(int(row['time'])/1000)))
                    day = int(time.strftime('%d',time.localtime(int(row['time'])/1000)))
                    content = str(row['content'])
                    likedcount = int(row['likedCount'])
                    nickname = str(row['user']['nickname'])
                    user_id = int(row['user']['userId'])
                    per_song.append({
                                    'index':count,
                                    'year':year,
                                    'month':month,
                                    'day':day,
                                    'content':content,
                                    'likecount':likedcount,
                                    'nickname':nickname,
                                    'user_id':user_id
                                    })
            except KeyError as e:
                if c == 'hotComments':
                    pass
                else:
                    print(e,song_name,doc['_id'])
        formated_data['%s-%s'%(song_name,song_id)] = per_song
    return formated_data

# 将格式化后的数据保存为csv文件
def save_csv(songs,path,formated_data):
    for song_name,song_id in songs:
        list = formated_data['{}-{}'.format(song_name,song_id)]
        try:
            with open('data/{}/{}-{}.csv'.format(path,song_name,song_id), 'w',encoding='utf-8') as f:
                w = csv.writer(f)
                fieldnames=list[0].keys()  # 写入第一行字段头部
                w.writerow(fieldnames)
                for row in list:
                    w.writerow(row.values())
            print('successfully save csv file of {}-{}'.format(song_name,song_id))
        except IndexError:
            print(list)
            print(song_name,song_id)


if __name__ == "__main__":
    ComDb= CommentsDb()
    songs = dataaudit.songs_indb(ComDb)#[('Leave','287546'),('Leave Me Alone','287769')]
    print(songs)
    formated = get_fromat(songs,ComDb,'hotComments')
    #print(formated)
    save_csv(songs,'hot',formated)
