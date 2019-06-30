import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from sklearn import linear_model
# 从csv中读入数据
user_info = pd.read_csv('user_info.csv')
follow = pd.read_csv('follow_new.csv')
#focol = pd.read_csv('focol_new.csv')

# 构建社交网络
G = nx.DiGraph() # 有向图
nodes = list(user_info['url_token'])
edges = list(follow.itertuples(index=False, name=None))
G.add_nodes_from(nodes)
G.add_edges_from(edges)

# 结点数与边数
print('结点数：', len(G.nodes()))
print('边数：', len(G.edges()))

# 度分布
def degree_distribution(G, degree):
    degree_dict = Counter(degree)
    del degree_dict[0] # 不考虑度数为0的结点
    x = np.array(list(degree_dict.keys())) # 度数
    y = np.array(list(degree_dict.values()))/len(G.nodes()) # 度数为k的结点数/总结点数
    regr = linear_model.LinearRegression() # 线性回归
    regr.fit(np.log(x).reshape(-1, 1), np.log(y))
    print('斜率：', regr.coef_, '截距：', regr.intercept_, 'R方：', regr.score(np.log(x).reshape(-1, 1), np.log(y)))
    plt.scatter(np.log(x).reshape(-1, 1), np.log(y), color='blue')
    plt.plot(np.log(x).reshape(-1, 1), regr.predict(np.log(x).reshape(-1, 1)), color='red')
    plt.show()


nx.draw(G)
plt.savefig("ba.png")
plt.show()