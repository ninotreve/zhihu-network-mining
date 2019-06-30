# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import mysql.connector
import json
from scrapy.exceptions import DropItem

class ZhihuPipeline(object):

    def __init__(self):
        self.id_seen = set()
        self.from_to_seen = set()
        self.from_url_seen = set()
        self.user_infoInsert = 'INSERT INTO user_info\
        (username, answer_count, articles_count, badge_identity, badge_best_answerer,\
        business, columns_count, favorite_count, favorited_count, follower_count,\
        following_columns_count, following_count, following_favlists_count,\
        following_question_count, following_topic_count, gender, hosted_live_count,\
        is_advertiser, is_org, logs_count, pins_count, question_count, thanked_count,\
        url_token, vip, voteup_count) VALUES (' + '%s,'*25 + '%s)'
        self.followInsert = 'INSERT INTO follow(from_id,to_id) VALUES (%s, %s)'
        self.focolInsert = 'INSERT INTO focol(from_id,to_url) VALUES (%s, %s)'

    def open_spider(self, spider):
        # 连接数据库
        self.connect = mysql.connector.connect(
            host = "127.0.0.1",
            database = "nina",
            user = "root",
            passwd = "vampire",
            auth_plugin='mysql_native_password')

        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()

    def process_item(self, item, spider):
        if item.__class__.__name__ == "UserItem":
            if item['url_token'] in self.id_seen:
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.id_seen.add(item['url_token'])
            self.cursor.execute(self.user_infoInsert,
            (item['name'],item['answer_count'],item['articles_count'],item['badge_identity'],
            item['badge_best_answerer'],item['business'],item['columns_count'],item['favorite_count'],
            item['favorited_count'],item['follower_count'],item['following_columns_count'],
            item['following_count'],item['following_favlists_count'],item['following_question_count'],
            item['following_topic_count'],item['gender'],item['hosted_live_count'],item['is_advertiser'],
            item['is_org'],item['logs_count'],item['pins_count'],item['question_count'],item['thanked_count'],
            item['url_token'],item['vip'],item['voteup_count']))
            self.connect.commit()
            print("记录插入成功。")
        elif item.__class__.__name__ == "FocolItem":
            if item['from_to'] in self.from_url_seen:
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.from_url_seen.add(item['from_to'])
            self.cursor.execute(self.focolInsert,
                (item["from_user"], item["to_url"]))
            self.connect.commit()
            print("记录插入成功。")
        elif item.__class__.__name__ == "FollowItem":
            if item['from_to'] in self.from_to_seen:
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.from_to_seen.add(item['from_to'])
            self.cursor.execute(self.followInsert,
                (item["from_user"], item["to_user"]))
            self.connect.commit()
            print("记录插入成功。")
        else:
            spider.log('Undefined name: %s' % spider.name)
        return item
