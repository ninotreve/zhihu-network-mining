# -*- coding: utf-8 -*-
import scrapy
import json
from zhihu.items import UserItem, FollowItem, FocolItem
import mysql.connector

import hmac
import time
import base64
from hashlib import sha1
import re

class ZhihuSpider(scrapy.Spider):
    name = 'zhihuspider'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    org_id = '36-ke' # 在这里输入官方号的id
    # org_url = 'https://www.zhihu.com/api/v4/members/{org_id}/followers?limit=20&offset={offset}'
    org_url = 'https://www.zhihu.com/api/v4/members/{org_id}/followers?include=data[*].follower_count&limit=20&offset={offset}' # 在第一次request中包含成员的粉丝信息
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
               'Referer': 'https://www.zhihu.com',
               'HOST': 'www.zhihu.com',
               'Authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20' }

    # 个人信息接口，使用.format方法来动态获取每个用户的信息
    user_info_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    # include 内容单独取出来
    user_query = '''
    name,answer_count,articles_count,badge,business,columns_count,follower_count,
    favorite_count,favorited_count,following_count,following_favlists_count,
    following_question_count,following_topic_count,following_columns_count,
    gender,hosted_live_count,is_advertiser,is_org,logs_count,pins_count,
    question_count,thanked_count,url_token,vip_info,voteup_count'''

    # 用户关注接口
    followee_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?limit=20&offset={offset}'
    # 用户粉丝接口
    follower_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?limit=20&offset={offset}'

    grant_type = 'password'
    client_id = 'c3cef7c66a1843f8b3a9e6a1e3160e20'
    source = 'com.zhihu.web'
    timestamp = str(int(time.time() * 1000))
    timestamp2 = str(time.time() * 1000)

    def get_signature(self, grant_type, client_id, source, timestamp):
        """处理签名"""
        hm = hmac.new(b'd1b964811afb40118a12068ff74a12f4', None, sha1)
        hm.update(str.encode(grant_type))
        hm.update(str.encode(client_id))
        hm.update(str.encode(source))
        hm.update(str.encode(timestamp))
        return str(hm.hexdigest())

    def parse(self, response):
        print(response.body.decode("utf-8"))

    def init_set(self):
        # 用户集合
        connect = mysql.connector.connect(
                host = "127.0.0.1",
                database = "zhihu",
                user = "root",
                passwd = "vampire",
                auth_plugin='mysql_native_password')
        cursor = connect.cursor()
        cursor.execute('SELECT url_token FROM zhihu.user_info;')
        if cursor is not None:
            result = cursor.fetchall()
            self.user_set = set(tup[0] for tup in result)
        assert len(self.user_set) != 0

    def init_list(self):
        # 大V列表
        connect = mysql.connector.connect(
                host = "127.0.0.1",
                database = "zhihu",
                user = "root",
                passwd = "vampire",
                auth_plugin='mysql_native_password')
        cursor = connect.cursor()
        cursor.execute('SELECT url_token FROM zhihu.user_info;')
        result = cursor.fetchall()
        self.bigv_list = [tup[0] for tup in result]
        assert len(self.bigv_list) != 0

    def start_requests(self):
        self.init_set()
        # self.init_list()
        yield scrapy.Request('https://www.zhihu.com/api/v3/oauth/captcha?lang=en',
                             headers=self.headers, callback=self.is_need_capture)

    def is_need_capture(self, response):
        print(response.text)
        need_cap = json.loads(response.body)['show_captcha']
        print(need_cap)

        if need_cap:
            print('需要验证码')
            yield scrapy.Request(
                url='https://www.zhihu.com/api/v3/oauth/captcha?lang=en',
                headers=self.headers,
                callback=self.capture,
                method='PUT'
            )
        else:
            print('不需要验证码')
            post_url = 'https://www.zhihu.com/api/v3/oauth/sign_in'
            post_data = {
                "client_id": self.client_id,
                "username": "18817729351",  # 输入知乎用户名
                "password": "mby971211",  # 输入知乎密码
                "grant_type": self.grant_type,
                "source": self.source,
                "timestamp": self.timestamp,
                "signature": self.get_signature(self.grant_type, self.client_id, self.source, self.timestamp),  # 获取签名
                "lang": "en",
                "ref_source": "homepage",
                "captcha": '',
                "utm_source": "baidu"
            }
            yield scrapy.FormRequest(
                url=post_url,
                formdata=post_data,
                headers=self.headers,
                callback=self.check_login
            )
        # yield scrapy.Request('https://www.zhihu.com/captcha.gif?r=%d&type=login' % (time.time() * 1000),
        #                      headers=self.headers, callback=self.capture, meta={"resp": response})
        # yield scrapy.Request('https://www.zhihu.com/api/v3/oauth/captcha?lang=en',
        #                      headers=self.headers, callback=self.capture, meta={"resp": response},dont_filter=True)

    def capture(self, response):
        # print(response.body)
        try:
            img = json.loads(response.body)['img_base64']
        except ValueError:
            print('获取img_base64的值失败！')
        else:
            img = img.encode('utf8')
            img_data = base64.b64decode(img)

            with open('zhihu03.gif', 'wb') as f:
                f.write(img_data)
                f.close()
        captcha = input('请输入验证码：')
        post_data = {
            'input_text': captcha
        }
        yield scrapy.FormRequest(
            url='https://www.zhihu.com/api/v3/oauth/captcha?lang=en',
            formdata=post_data,
            callback=self.captcha_login,
            headers=self.headers
        )

    def captcha_login(self, response):
        try:
            cap_result = json.loads(response.body)['success']
            print(cap_result)
        except ValueError:
            print('关于验证码的POST请求响应失败!')
        else:
            if cap_result:
                print('验证成功!')

        post_url = 'https://www.zhihu.com/api/v3/oauth/sign_in'
        post_data = {
            "client_id": self.client_id,
            "username": "18817729351",  # 输入知乎用户名
            "password": "mby971211",  # 输入知乎密码
            "grant_type": self.grant_type,
            "source": self.source,
            "timestamp": self.timestamp,
            "signature": self.get_signature(self.grant_type, self.client_id, self.source, self.timestamp),  # 获取签名
            "lang": "en",
            "ref_source": "homepage",
            "captcha": '',
            "utm_source": ""
        }
        headers = self.headers
        headers.update({
            'Origin': 'https://www.zhihu.com',
            'Pragma': 'no - cache',
            'Cache-Control': 'no - cache'
        })
        yield scrapy.FormRequest(
            url=post_url,
            formdata=post_data,
            headers=headers,
            callback=self.check_login
        )

    def check_login(self, response):
        # 验证是否登录成功
        text_json = json.loads(response.text)
        print('登陆成功！', text_json)
        yield scrapy.Request(self.org_url.format(org_id=self.org_id, offset=40000),
                             callback=self.org_parse, headers=self.headers)
        # for bigv in self.bigv_list:
        #     # 解析每个大v的关注
        #     yield scrapy.Request(self.followee_url.format(user=bigv, offset=0), callback=self.followee_info_parse,
        #                          headers=self.headers)

    def org_parse(self, response):
        '''获取机构的关注者'''
        result = json.loads(response.text)
        if 'data' in result.keys():
            for user in result.get('data'):
                # 测试用户是否是大v，粉丝大于10000
                followers = user.get('follower_count')
                if followers > 5000:
                    continue
                yield scrapy.Request(self.user_info_url.format(user=user.get('url_token'), include=self.user_query),
                              callback=self.user_info_parse)

        # 如果有下一页，则重复调用org_parse
        if 'paging' in result.keys() and result.get('paging').get('is_end') == False:
            offset = int(re.findall('\d+$',response.url)[0])
            offset += 20
            if offset < 80000: # 先爬80000个试试水
                yield scrapy.Request(self.org_url.format(org_id=self.org_id,
                                     offset=offset), callback=self.org_parse)

    def user_info_parse(self, response):
        '''获取用户个人信息， 大V only:) # 现在是只有非大v才能进！'''

        # 将获取到的Python对象转换为json对象
        result = json.loads(response.text)

        self.user_set.add(result.get('url_token'))
        # 实例化一个UserItem用来传递信息
        item = UserItem()
        for key in result.keys():
            if key == 'badge':
                item['badge_identity'] = False
                item['badge_best_answerer'] = False
                badge_list = result.get('badge')
                for badge in badge_list:
                    new_key= 'badge_' + badge.get('type')
                    item[new_key] = True
            elif key == 'vip_info':
                item['vip'] = result.get('vip_info').get('is_vip')
            elif key == 'business':
                item['business'] = result.get('business').get('name')
            elif key in item.fields:
                item[key] = result.get(key)
            else:
                continue
        if item.get('vip') is None:
            item['vip'] = None
        yield item

        # 将url_token传递给获取用户关注的函数
        yield scrapy.Request(self.followee_url.format(user=result['url_token'],
            offset=0), callback=self.followee_info_parse)
        yield scrapy.Request(self.follower_url.format(user=result['url_token'],
            offset=0), callback=self.follower_info_parse)
            # yield scrapy.Request(self.focolumn_url.format(user=result['url_token'],
            #     offset=0, limit=20), callback=self.focolumn_info_parse)

    def followee_info_parse(self, response):
        '''获取用户的关注'''
        self_id = response.url.split('/')[6] # 此用户的id
        result = json.loads(response.text)
        if 'data' in result.keys():
            for user in result.get('data'):
                # 如果用户在user_set中才加入
                if user.get('url_token') in self.user_set:
                # # 如果用户在bigv_list中才加入
                # if user.get('url_token') in self.bigv_list:
                    # 实例化一个FollowItem
                    item = FollowItem()
                    item['from_user'] = self_id
                    item['to_user'] =  user.get('url_token')
                    item['from_to'] = item['from_user'] + item['to_user']
                    yield item

        # 如果有下一页，则重复调用followee_info_parse
        if 'paging' in result.keys() and result.get('paging').get('is_end') == False:
            offset = int(re.findall('\d+$',response.url)[0])
            offset += 20
            yield scrapy.Request(self.followee_url.format(user=self_id,
                offset=offset), callback=self.followee_info_parse)

    def follower_info_parse(self, response):
        '''获取用户的粉丝'''
        self_id = response.url.split('/')[6] # 此用户的id
        result = json.loads(response.text)
        if 'data' in result.keys():
            for user in result.get('data'):
                # 如果用户在user_set中才加入
                if user.get('url_token') in self.user_set:
                    # 实例化一个FollowItem
                    item = FollowItem()
                    item['from_user'] = user.get('url_token')
                    item['to_user'] = self_id
                    item['from_to'] = item['from_user'] + item['to_user']
                    yield item

        # 如果有下一页，则重复调用follower_info_parse(经过修改)
        if 'paging' in result.keys() and result.get('paging').get('is_end') == False:
            offset = int(re.findall('\d+$',response.url)[0])
            offset += 20
            yield scrapy.Request(self.follower_url.format(user=self_id,
                offset=offset), callback=self.follower_info_parse)

    # def focolumn_info_parse(self, response):
        # '''获取用户的关注'''
        # self_id = response.url[37:-18] # 此用户的id
        # result = json.loads(response.text)
        # if 'data' in result.keys():
        #     for column in result.get('data'):
        #         # 实例化一个FocolItem
        #         item = FocolItem()
        #         item['from_user'] = self_id
        #         item['to_url'] =  column.get('id')
        #         item['from_to'] = item['from_user'] + item['to_url']
        #         yield item
        #
        # # 如果有下一页，则重复调用focolumn_info_parse
        # if 'paging' in result.keys() and result.get('paging').get('is_end') == False:
        #     next_url = result.get('paging').get('next')
        #     yield scrapy.Request(next_url, callback=self.focolumn_info_parse)
