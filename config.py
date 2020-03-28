#!/usr/bin env python
# coding = utf-8

#database config on mongo
db_port = 27017
db_host = 'localhost'

#'cookie': '_iuqxldmzr_=32; _ntes_nnid=1c2596d3ac02e635bdcdaf4d636075af,1566872282395; _ntes_nuid=1c2596d3ac02e635bdcdaf4d636075af; WM_NI=ElosMGV%2BkohPPuBlo%2BWRcHyLibA38NwlqWtKX4a9npA3yd4g76n%2Fmm0XnZ3dBnWEZ6Zg5pPPsNeAuRx5%2Bc1t8deMqQXUW7DWfHZH5%2F3ULG1sMgYjoIoURtv8PRa3PaiKa28%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6ee8eea3ca2f0ffaecd7b8eeb8ab3d44e868f8e85bc33a3879a95b66f9bee89adef2af0fea7c3b92a87b4a194d04d96f5a590eb5c94ab8e8dee21958eada9fc48abbe8fd4bb46b5b4bfb8f7419cecafdaed7c83edb785b76df5eaa2d0f067f488a2bbb27082b299a6d93e9ab9fb91d35cb192aba2f85abcebe584b480fcbcabaef45b9c8b99d8c75da69896a9b825f18b84a8b4798fb9978bee43ad8b9e95f534948eafd4d36bab95afd3bb37e2a3; WM_TID=I%2BJIVhPUtYlAVAEFARNpoacB8vaNjSL1; ntes_kaola_ad=1; JSESSIONID-WYYY=JVSBQ4FNFrVr7opN4mtR%2BFsiZ6pHBqux8VMDV%2BYQU%5CK0W4Dkv0wF7vIq1JUW%5C6bmugs%2FzQONIa3%2Bu7eWdEpIvJYsP39gcAlB5zwoaO5Y431Y%2BC1EcPbaqXeXwra3oQNaXeV70E3dBZgSY3oZKht%5C%2BjzlbuzHDgRDKQIyKvHxrP3VcVE8%3A1566877564022',
#dataspider config
baseurl = 'https://music.163.com'
singername = '孙燕姿'
singer_id = '9272'
singer_url = '/artist/album?id=%s&limit=10000'%(singer_id)
headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'referer': 'https://music.163.com/',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': '' #暂时置空，在spider中随机伪造
        }

comments_url = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_1379481976?csrf_token='