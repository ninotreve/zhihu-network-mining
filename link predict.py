import networkx as nx
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import random
def my_jaccard(G,from_id,to_id):
    nbrs = list(G.neighbors(from_id))
    nbrs_nbrs = []
    for nbr in nbrs:
        nbrs_nbrs = nbrs_nbrs + list(G.neighbors(nbr))
    nbrs_nbrs_set = set(nbrs_nbrs)
    try:
        leader = list(G.neighbors(to_id))
    except Exception:
        return 0
    leader_set = set(leader)
    try:
        jaccard_coefficient = len(nbrs_nbrs_set&leader_set)/float(len(nbrs_nbrs_set|leader_set))
    except ZeroDivisionError :
        jaccard_coefficient = 0
    return jaccard_coefficient

df = pd.read_csv('all_follow.csv')
print("数据读取结束，开始构建图")
all_array = np.array(df)
np.random.shuffle(all_array)
n = len(df)
train_array = all_array[:int(n*0.95)]
test_array = all_array[int(n*0.95):]
#读取follower边集合
df = pd.read_csv('ke_leaders_follower.csv')
follow_array = np.array(df)
# np.random.shuffle(follow_array)
# n = len(df)
# train_array = follow_array[:int(n*0.95)]
# test_array = follow_array[int(n*0.95):]
#读入leader边集合
df = pd.read_csv('ke_leader.csv')
leader_array = np.array(df)
# np.random.shuffle(leader_array)
# n = len(df)
# train_array = leader_array[:int(n*0.95)]
# test_array = leader_array[int(n*0.95):]

print("数据读取结束，开始构建图")

#读取sample边集合
df = pd.read_csv('sample.csv')
sample_array = np.array(df)


G0 = nx.Graph()
G0.add_edges_from(all_array)

G = nx.Graph()
G.add_edges_from(train_array)
# G.add_edges_from(leader_array)
G.add_nodes_from(G0.nodes)
print("图构建结束，共%d个节点"%G.number_of_nodes())
result_list = []
large = 0

for i in range(int(n*0.05)):
    if i%10 == 0:
        print(i)
    a, b = sample_array[i]
    from_id, to_id = test_array[i]
    preds_unexist = my_jaccard(G,a,b)
    preds_exist = my_jaccard(G,from_id,to_id)
    if preds_exist>preds_unexist:
        large+=1
    elif abs(preds_exist-preds_unexist)<1e-6:
        large+=0.5
    print(large/float(i+1))

print(large/float(int(n*0.05)))
