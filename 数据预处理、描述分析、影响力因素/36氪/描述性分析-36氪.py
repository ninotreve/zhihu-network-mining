
# coding: utf-8

# # 36氪-描述性分析

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
pd.set_option('display.max_columns', None)


# In[2]:


df_kr = pd.read_csv('./36kr_final.csv')


# In[3]:


df_kr.head()


# In[4]:


df_kr.columns.tolist()


# ### 描述性统计

# ### 一、基本情况

# In[5]:


df_kr.describe()


# - 36氪的粉丝共245074人
# - 其他的如果需要放ppt里可以做个表列出来

# In[6]:


# 回答数最多
df_kr.loc[df_kr['answer_count'] == df_kr['answer_count'].max(), :]


# In[7]:


# 文章数最多
df_kr.loc[df_kr['articles_count'] == df_kr['articles_count'].max(), :]


# In[8]:


# 参与公共编辑数最多
df_kr.loc[df_kr['logs_count'] == df_kr['logs_count'].max(), :]


# In[9]:


# 关注数最多
df_kr.loc[df_kr['following_count'] == df_kr['following_count'].max(), :]


# In[10]:


# 关注话题数最多
df_kr.loc[df_kr['following_topic_count'] == df_kr['following_topic_count'].max(), :]


# In[11]:


# 粉丝数最多
df_kr.loc[df_kr['follower_count'] == df_kr['follower_count'].max(), :]


# #### 图：回答数、文章数、关注数、关注话题数的分布

# In[12]:


f, axes = plt.subplots(2, 3, figsize=(15, 8), sharex=True)
sns.distplot(np.log10(df_kr['answer_count'] + 1), ax=axes[0, 0])
axes[0, 0].set(xlabel='log_answer_count')
sns.distplot(np.log10(df_kr['articles_count'] + 1), ax=axes[0, 1])
axes[0, 1].set(xlabel='log_articles_count')
sns.distplot(np.log10(df_kr['logs_count'] + 1), ax=axes[0, 2])
axes[0, 2].set(xlabel='log_logs_count')

sns.distplot(np.log10(df_kr['following_count'] + 1), ax=axes[1, 0])
axes[1, 0].set(xlabel='log_following_count')
sns.distplot(np.log10(df_kr['following_topic_count'] + 1), ax=axes[1, 1])
axes[1, 1].set(xlabel='log_following_topic_count')
sns.distplot(np.log10(df_kr['follower_count'] + 1), ax=axes[1, 2])
axes[1, 2].set(xlabel='log_follower_count');  


# - 上面图：对数回答数、对数文章数、对数参与公共编辑数的分布，可以发现，分布呈明显的右偏，36氪大部分的粉丝，基本都不怎么回答问题，不怎么发文章，较少参与公共编辑；
# - 左下两张图：对数关注数和对数关注话题数的分布，人们尽管不怎么回答问题，发表文章，但多多少少都会关注一些用户或话题；
# - 可以从中一窥知乎的特点：大部分用户都是来”围观“，来知乎“寻找答案”，只有少数用户（很可能是某个领域的专业人士）才会踊跃发言。从右下的对数粉丝数分布也可以推测出，那些少数踊跃发言的用户拥有大量的粉丝，而大多数的用户粉丝数并不多。

# ### 二、按分类变量探索

# #### （一）认证用户

# In[13]:


print('认证用户：', df_kr.loc[(df_kr['badge_identity'] == 1),].shape[0])


# In[14]:


df_kr.loc[(df_kr['badge_identity'] == 1), 'username'].tolist()


# #### （二）优秀回答者

# In[15]:


df_kr.loc[df_kr['badge_best_answerer'] == 1,].shape[0]


# In[16]:


df_kr.loc[df_kr['badge_best_answerer'] == 1, 'username'].tolist()


# #### （三）性别

# ##### 总体情况

# In[17]:


df_kr['gender'].value_counts()


# In[18]:


# Plot
labels = 'unknown', 'male', 'female', 'is_org'
sizes = df_kr['gender'].value_counts().values
colors = ['lightskyblue', 'yellowgreen', 'gold', 'lightcoral']
explode = (0, 0.1, 0, 0)  # explode 1st slice

plt.pie(sizes, explode = explode, labels=labels, colors=colors,
autopct='%1.1f%%', shadow=True, startangle=140)

plt.axis('equal')
plt.show()


# - 填写了性别的用户，男性比例比女性高

# ##### 粉丝数大于1w用户

# In[20]:


df_kr.loc[df_kr['follower_count'] > 10000, 'gender'].value_counts()


# In[21]:


# Plot
labels = 'male', 'female', 'is_org', 'unknown'
sizes = df_kr.loc[df_kr['follower_count'] > 10000, 'gender'].value_counts().values
colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
explode = (0, 0.1, 0, 0)  # explode 1st slice

plt.pie(sizes, explode = explode, labels=labels, colors=colors,
autopct='%1.1f%%', shadow=True, startangle=140)

plt.axis('equal')
plt.show()


# - 关注36氪的大V中男性比例远高于女性

# #### （四）广告主

# In[22]:


# 个数
df_kr.loc[df_kr['is_advertiser'] == 1, ].shape[0]


# In[23]:


# 分别是
df_kr.loc[df_kr['is_advertiser'] == 1, 'username']


# #### （五）组织机构

# In[24]:


# 个数
df_kr.loc[df_kr['is_org'] == 1, ].shape[0]


# In[25]:


df_kr.loc[
    df_kr['is_org'] == 1, ('username','follower_count')
].to_csv('36kr_org_wordcloud.csv', index = False)


# #### （六）行业 (合并后SIC)

# In[28]:


labels = df_kr['SIC'].value_counts().index 
values = df_kr['SIC'].value_counts().values 

trace = go.Pie(labels=labels, values=values)
layout = go.Layout(
    autosize=False,
    width=500,
    height=500)
py.iplot([trace], filename='basic_pie_chart')

