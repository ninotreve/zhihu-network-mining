'''visualize degree distribution'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model

df = pd.read_csv("xinli_leader_analysis.csv",encoding="utf-8")#改成文件名字
user_degree = []
for i in range(len(df)-1):
    user_degree.append(df.loc[i, 'degree'])#这里如果是处理过的数据文件就直接degree

    # ind = user_degree.append(df.loc[i, 'follower_count'])  #如果是原始文件的话用下面的代码
    # outd = user_degree.append(df.loc[i, 'following_count'])
    # if ind is None:
    #     continue
    # if outd is None:
    #     continue
    # if outd+ind == 0:
    #     continue
    # user_degree.append(ind+outd)
user_degree=np.array(user_degree)
user_degree.sort()
x=[]
y=[]
# 去重
no_duplicate = list(set(user_degree))
dic = {}
for key in user_degree:
    dic[key] = dic.get(key, 0) + 1
x = no_duplicate[1:]
y = list(dic.values())[1:]

regr = linear_model.LinearRegression()  # 线性回归
regr.fit(np.log(x).reshape(-1, 1), np.log(y))
print('斜率：', regr.coef_, '截距：', regr.intercept_, 'R方：', regr.score(np.log(x).reshape(-1, 1), np.log(y)))
plt.scatter(np.log(x).reshape(-1, 1), np.log(y), color='blue')
plt.plot(np.log(x).reshape(-1, 1), regr.predict(np.log(x).reshape(-1, 1)), color='red')

fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(x=x,y=y)
plt.title('degree distribution')
plt.yscale('log')
plt.xscale('log')
plt.xlabel('Degree')
plt.ylabel('number')
plt.show()
