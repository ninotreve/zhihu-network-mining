
# coding: utf-8

# # 36氪-影响力因素分析

# In[11]:


import pandas as pd
import numpy as np
import seaborn as sns
pd.set_option('display.max_columns', None)
import warnings
warnings.filterwarnings("ignore")
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt


# In[12]:


df_kr = pd.read_csv('./36kr_final.csv')


# In[13]:


df_kr.head()


# In[14]:


df_kr.describe()


# ## pagerank

# #### (一)查看分布情况

# In[15]:


df_kr['pageranks'].describe()


# In[16]:


sns.distplot(np.log10(df_kr['pageranks'] + 0.000000000001),kde = False);


# In[17]:


df_kr.loc[df_kr['pageranks'] > 0.000001, :].shape


# In[18]:


df_kr.loc[df_kr['pageranks'] > 0.000001, :].shape[0] / df_kr.shape[0]


# #### （二）定义pagerank大于0.000001为影响力高

# In[19]:


df_kr['influence'] = 0
df_kr.loc[df_kr['pageranks'] > 0.000001, 'influence'] = 1


# ## 随机森林

# #### （一）特征

# In[20]:


df_kr.columns.tolist()


# In[21]:


df_input = df_kr.loc[:, ( 'answer_count',
 'articles_count',
 'badge_identity',
#  'badge_best_answerer',
 'columns_count',
 'favorite_count',
 'favorited_count',
#  'follower_count',
 'following_columns_count',
 'following_count',
 'following_favlists_count',
 'following_question_count',
 'following_topic_count',
#  'gender',
 'hosted_live_count',
 'is_advertiser',
 'is_org',
#  'logs_count',
 'pins_count',
 'question_count',
 'thanked_count',
 'vip',
 'voteup_count',
)]
df_sic_dummy = pd.get_dummies(df_kr['SIC']).drop('unknown', axis = 1)


# In[22]:


X = pd.concat([df_input, df_sic_dummy], axis = 1)
y = df_kr['influence']


# #### （二）将数据划分为：0.6训练集 0.2验证集  0.2测试集

# In[23]:


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=1, stratify = y)
X_train, X_val, y_train, y_val = train_test_split(
    X_train, y_train, test_size=0.25, random_state=1, stratify = y_train)


# #### （三）样本不均衡，SMOTE

# In[24]:


from collections import Counter
from imblearn import over_sampling
from imblearn.over_sampling import SMOTE

print('Original dataset shape %s' % Counter(y_train))

sm = SMOTE(random_state=42)
X_res, y_res = sm.fit_sample(X_train, y_train)
print('Resampled dataset shape %s' % Counter(y_res))


# #### （四）随机森林

# In[25]:


for n_estimators in (50, 70, 100):  
    for max_depth in (4, 8, 10, 30, 50, 70, 100):
        clf = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth,
                                     random_state=10)
        clf.fit(X_res, y_res)  
        y_val_pred = clf.predict(X_val)
        y_val_pred_prob = clf.predict_proba(X_val)
        print('n_estimators:', n_estimators,
              'max_depth:', max_depth, 
              'auc:', roc_auc_score(y_val, y_val_pred_prob[:,1]))
        print(confusion_matrix(y_val, y_val_pred))


# In[26]:


# test
clf = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=10)
clf.fit(X_res, y_res)  
y_test_pred = clf.predict(X_test)
y_test_pred_prob = clf.predict_proba(X_test)
roc_auc_score(y_test, clf.predict_proba(X_test)[:,1])


# #### （五）Feature importance

# In[27]:


for name, importance in zip(X.columns, clf.feature_importances_):
    print(name, "=", importance)


# In[28]:


fig, ax = plt.subplots()
feat_importances = pd.Series(clf.feature_importances_, index=X.columns)
ax = feat_importances.nlargest(10).plot(kind='barh',title = "Features Importance", color='#3399FF')
ax.invert_yaxis();

