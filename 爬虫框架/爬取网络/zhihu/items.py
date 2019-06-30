# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UserItem(scrapy.Item):
    # 用户个人信息，主要收集一些数值变量，共25个
    name = scrapy.Field() #姓名
    answer_count = scrapy.Field() #回答数
    articles_count = scrapy.Field() #文章数
    badge_identity = scrapy.Field() #是认证用户
    badge_best_answerer = scrapy.Field() #是优秀回答者
    business = scrapy.Field() # 领域
    columns_count = scrapy.Field() #专栏数
    favorite_count = scrapy.Field() #收藏数
    favorited_count = scrapy.Field() #被收藏数
    follower_count = scrapy.Field() #粉丝数
    following_columns_count = scrapy.Field() #关注的专栏数
    following_count = scrapy.Field() #关注用户数
    following_favlists_count = scrapy.Field() #关注的收藏数
    following_question_count = scrapy.Field() #关注的问题数
    following_topic_count = scrapy.Field() #关注的话题数
    gender = scrapy.Field() #性别
    hosted_live_count = scrapy.Field() #举办的Live数
    is_advertiser = scrapy.Field() #是广告主
    is_org = scrapy.Field() #是组织机构
    logs_count = scrapy.Field() #参与公共编辑数
    pins_count = scrapy.Field() #想法数
    question_count = scrapy.Field() #提问数
    thanked_count = scrapy.Field() #被感谢数
    url_token = scrapy.Field() #知乎用户名
    vip = scrapy.Field() #是否是vip
    voteup_count = scrapy.Field() #被赞同数

class FollowItem(scrapy.Item):
    # 用户互相关注信息
    from_user = scrapy.Field()
    to_user = scrapy.Field()
    from_to = scrapy.Field()

class FocolItem(scrapy.Item):
    # 用户关注专栏信息
    from_user = scrapy.Field()
    to_url = scrapy.Field()
    from_to = scrapy.Field()
