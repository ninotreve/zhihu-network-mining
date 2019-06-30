import networkx as nx
import pandas as pd
import numpy as np
import random
df = pd.read_csv('all_follow.csv')
print("数据读取结束，开始构建图")
all_array = np.array(df)
exist_set = set()
for i in all_array.tolist():
    exist_set.add(tuple(i))
G = nx.Graph()
G.add_edges_from(all_array)

#读入leader边集合
df = pd.read_csv('ke_leader.csv')
leader_array = np.array(df)
G0 = nx.Graph()
G0.add_edges_from(leader_array)

follower_list = [ i for i in G.nodes() if i not in G0.nodes()]
select = zip(random.sample(follower_list,100),random.sample(G0.nodes(),100))
select = [i for i in select if i not in exist_set]
select_array = np.array(select)
for i in range(1000):
    print(i)
    select = zip(random.sample(follower_list, 100), random.sample(G0.nodes(), 100))
    select = [i for i in select if i not in exist_set]
    select_array = np.vstack((select_array,np.array(select)))
df = pd.DataFrame(select_array)
df.to_csv("sample.csv",encoding='utf-8',index=False)