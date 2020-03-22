#!/usr/bin/env python
#coding = utf-8

import re
import json
import base64
import requests
import config
import fake_useragent
from requests.exceptions import RequestException
from pyquery import PyQuery as pq
from Crypto.Cipher import AES


class CommentsSpider():
    '''
    @Description:
    post加密部分参考了知乎@平胸小仙女的文章(地址:https://www.zhihu.com/question/36081767)
    评论爬虫类，只开放三个接口：
        get_album_id_and_name(self)
        get_song_id_and_name(self,album_url)
        get_comments(self,song_id,offset)
    '''
    def __init__(self,singer_id,offset, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__singer_album_url = config.baseurl + '/artist/album?id=%s&limit=10000'%(singer_id)
        self.__headers = config.headers

        #四个获取评论所需的待处理参数
        #self.first_param = "{{rid:\"\", offset:\"{offset}\", total:\"true\", limit:\"100\", csrf_token:\"\"}}".format(offset = offset)
        #self.__second_param = "010001"
        #self.__third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
        #self.__forth_param = "0CoJUm6Qyw8W8jud"

        


    def __get_singer_album_page(self):
        try:
            response = requests.get(self.__singer_album_url, headers=self.__headers)
            if response.status_code == 200:
                return response.text
            return None
        except RequestException:
            return None


    def get_albums_id(self):
        '''拿到专辑id列表'''
        singer_album_html = self.__get_singer_album_page()
        html = pq(singer_album_html)
        albums_id = [i.attr('data-res-id') for i in html('#m-song-module').find('li').items('a.icon-play.f-alpha')]
        albums_name = [i.attr('title') for i in html('#m-song-module').find('li').items('div.u-cover.u-cover-alb3')]
        for i in zip(albums_name,albums_id):
            yield i

    def __get_album_page(self,album_id):
        try:
            album_url = config.baseurl + '/album?id=%s'%(album_id)
            response = requests.get(album_url, headers=self.__headers)
            if response.status_code == 200:
                return response.text
            return None
        except RequestException:
            return None


    def get_songs_id(self,album_id):
        '''拿到歌曲id列表'''
        album_html = self.__get_album_page(album_id)
        pattern = re.compile(r'title=(.*);url=https://music.163.com/song\?id=(\d*)')
        for i in re.findall(pattern, album_html):
            yield i

    def get_total(self,song_id):
        pass


    def __AES_encrypt(self,text, key, iv):
        '''aes加密'''
        text = text.decode('utf-8')
        pad = 16 - len(text) % 16
        text = text + pad * chr(pad)
        encryptor = AES.new(key, AES.MODE_CBC, iv)
        encrypt_text = encryptor.encrypt(text.encode())
        encrypt_text = base64.b64encode(encrypt_text)
        return encrypt_text


    def __get_params(self,offset):
        '''得到异步加载评论所需的第一个参数'''
        first_param = "{{rid:\"\", offset:\"{offset}\", total:\"true\", limit:\"20\", csrf_token:\"\"}}".format(offset = offset)
        forth_param = "0CoJUm6Qyw8W8jud"
        iv = "0102030405060708"
        first_key = forth_param
        second_key = 16 * 'F'
        h_encText = self.__AES_encrypt(first_param.encode(),first_key.encode(), iv.encode())
        h_encText = self.__AES_encrypt(h_encText, second_key.encode(),iv.encode()).decode('utf-8')
        return h_encText


    def __get_encSecKey(self):
        '''拿到异步加载评论所需的第二个参数'''
        encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
        return encSecKey

    def __get_proxy(self):
        return requests.get("http://127.0.0.1:5010/get/").json()

    def __delete_proxy(self,proxy):
        requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

    def __wrap_header(self):
        try:
            user_agent = fake_useragent.UserAgent()
            ua = user_agent.random
        except Exception:
            ua = r'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400'
        finally:
            self.__headers['user-agent'] = ua
            return self.__headers

    def get_comments(self,song_id,offset):
        '''根据song_id拿到包含评论的字典，每次返回20条数据'''
        params = self.__get_params(offset)
        encSecKey = self.__get_encSecKey()
        proxy = self.__get_proxy().get("proxy")
        comments_url = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_%s?csrf_token='%(song_id)
        data = { "params": params, "encSecKey": encSecKey } 
        retry_count = 5
        while retry_count > 0:
            try:
                response = requests.post(comments_url, headers=self.__wrap_header(), proxies={"http": "http://{}".format(proxy)},data=data,timeout=10)
                if response.status_code == 200:
                    print(response.request.headers['user-agent'])
                    print('using proxy',proxy)
                    com_dict = json.loads(response.content)
                    #print(com_dict)
                    return com_dict
            except RequestException:
                retry_count -= 1
        self.__delete_proxy(proxy)
        return {'total':0}



