
# coding: utf-8

# # 数据预处理-36氪

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib as mpl
import plotly.plotly as py
import plotly.graph_objs as go
import warnings
warnings.filterwarnings("ignore")


# In[2]:


df_kr = pd.read_csv('./ke_user_info.csv')


# In[3]:


df_kr.head()


# In[4]:


df_kr.drop('id',axis=1,inplace=True)

df_kr.rename({'url_token': 'Id'}, axis=1, inplace = True)


# In[5]:


df_kr = df_kr[['Id',
 'username',
 'answer_count',
 'articles_count',
 'badge_identity',
 'badge_best_answerer',
 'business',
 'columns_count',
 'favorite_count',
 'favorited_count',
 'follower_count',
 'following_columns_count',
 'following_count',
 'following_favlists_count',
 'following_question_count',
 'following_topic_count',
 'gender',
 'hosted_live_count',
 'is_advertiser',
 'is_org',
 'logs_count',
 'pins_count',
 'question_count',
 'thanked_count',
 'vip',
 'voteup_count']]


# In[6]:


df_kr.head()


# #### 与统计表合并,加上pageranks列

# In[7]:


df_pagerank = pd.read_csv('./ke_all_analysis.csv').loc[:,('Id','pageranks')]
df_pagerank.head()


# In[8]:


df_kr = df_kr.merge(df_pagerank, on='Id', how='left')

p = (1 - 0.85)/ df_kr.shape[0]
df_kr['pageranks'].fillna(p, inplace = True)


# #### 组织机构的性别改成-2

# In[9]:


# 组织机构的性别全是-1.我把他改成-2，以跟unknown的区分
# df_kr.loc[df_kr['is_org'] == 1, 'gender'].value_counts()
df_kr.loc[df_kr['is_org'] == 1, 'gender'] = -2


# #### 把行业合并 SIC

# In[10]:


xxcs = [
    '互联网',
    '计算机软件',
    '电子商务',
    '通信',
    '电子游戏',
    '计算机硬件']
df_kr.loc[df_kr.business.isin(xxcs), 'SIC'] = '信息传输、计算机服务和软件业'

jtys = [
    '铁路运输',
    '地面运输',
    '交通仓储',
    '物流递送',
    '航运业',
    '管线运输',
    '邮政']
df_kr.loc[df_kr.business.isin(jtys), 'SIC'] = '交通运输、仓储和邮政业'

edu = [
    '高等教育',
    '基础教育',
    '教育',
    '培训',
    '幼儿教育',
    '职业教育',
    '特殊教育']
df_kr.loc[df_kr.business.isin(edu), 'SIC'] = '教育'

jinrong = [
    '金融',
    '财务',
    '银行',
    '资本投资',
    '证券投资',
    '保险',
    '信贷']
df_kr.loc[df_kr.business.isin(jinrong), 'SIC'] = '金融业'

nongye = [
    '种植业',
    '畜牧养殖业',
    '林业',
    '渔业',
    '农林牧渔']
df_kr.loc[df_kr.business.isin(nongye), 'SIC'] = '农、林、牧、渔业'

wenhua = [
    '创意艺术',
    '广播电视',
    '信息传媒',
    '旅游',
    '艺术娱乐',
    '图书馆',
    '娱乐休闲',
    '出版业',
    '体育健身',
    '博物馆',
    '博彩',
    '电影录音',
    '策展']
df_kr.loc[df_kr.business.isin(wenhua), 'SIC'] = '文化、体育和娱乐业'

keji = [
    '高新科技',
    '科研',
    '生物工程']
df_kr.loc[df_kr.business.isin(keji), 'SIC'] = '科学研究和技术服务业'

pifa = [
    '进出口贸易',
    '零售',
    '贸易零售']
df_kr.loc[df_kr.business.isin(pifa), 'SIC'] = '批发和零售'

yiyao = [
    '临床医疗',
    '制药',
    '医疗服务',
    '医疗器材']
df_kr.loc[df_kr.business.isin(yiyao), 'SIC'] = '医药卫生'

qiche = ['汽车']
df_kr.loc[df_kr.business.isin(qiche), 'SIC'] = '汽车业'

fuwu = [
    '法律',
    '广告',
    '咨询分析',
    '市场推广',
    '审计',
    '服务业',
    '公关']
df_kr.loc[df_kr.business.isin(fuwu), 'SIC'] = '租赁和商务服务'

fdc = ['房地产']
df_kr.loc[df_kr.business.isin(fdc), 'SIC'] = '房地产业'

zzy = [
    '机械设备',
    '电子电器',
    '建筑设备',
    '制造加工',
    '化工业',
    '塑料工业',
    '印刷业',
    '烟草业',
    '石油工业',
    '造纸业']
df_kr.loc[df_kr.business.isin(zzy), 'SIC'] = '制造业'

cky = [
    '有色金属',
    '煤炭工业',
    '开采冶金',
    '黑色金属',
    '土砂石开采',
    '金属加工',
    '地热开采']
df_kr.loc[df_kr.business.isin(cky), 'SIC'] = '采矿业'

gg = [
    '政府',
    '非营利组织',
    '社工服务',
    '公共管理',
    '公共服务']
df_kr.loc[df_kr.business.isin(gg), 'SIC'] = '公共管理和社会组织'

zhusu = [
    '餐饮',
    '酒店']
df_kr.loc[df_kr.business.isin(zhusu), 'SIC'] = '住宿和餐饮业'

dian = ['电力电网']
df_kr.loc[df_kr.business.isin(dian), 'SIC'] = '电力、燃气及水的生产和供应'

qt = [
    '人力资源',
    '军火',
    '装饰装潢',
    '环境保护',
    '食品饮料业',
    '养老服务',
    '服装业',
    '纺织皮革业',
    '民用航空业',
    '保健',
    '国防军事',
    '疗养服务',
    '物业服务',
    '景观',
    '护理服务',
    '特殊建造',
    '水利能源',
    '给排水',
    '航天',
    '美容',
    '家具',
    '大宗交易',
    '地产建筑',
    '有色金属',
    '煤炭工业',
    '开采冶金',
    '黑色金属',
    '土砂石开采',
    '金属加工',
    '地热开采']
df_kr.loc[df_kr.business.isin(qt), 'SIC'] = '其他'

df_kr.loc[df_kr['business'].isnull(),'SIC'] = 'unknown'
df_kr.loc[df_kr['business'] == '????','SIC'] = 'unknown'


# In[11]:


df_kr['SIC'].value_counts()


# #### vip

# In[12]:


df_kr.loc[df_kr['vip'] == '0', 'vip'] = 0
df_kr.loc[df_kr['vip'] == '1', 'vip'] = 1
df_kr.loc[(df_kr['vip'] != 0) & (df_kr['vip'] != 1), 'vip'] = 0


# In[13]:


df_kr.to_csv('36kr_final.csv', index = False)

