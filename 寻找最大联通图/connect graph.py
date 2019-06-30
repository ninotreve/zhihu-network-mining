'''find the largest connect graph'''
import pandas as pd
import numpy as np

df = pd.read_csv("all_follow.csv")#改成文件名字
connect_set = set()
select_list = []
left_list = []
all_array = np.array(df)
for i in range(len(all_array)-1):
    p1, p2 = tuple(all_array[i])
    if p1 in connect_set or p2 in connect_set:
        select_list.append(i)
    else:
        left_list.append(i)
    connect_set.add(p1)
    connect_set.add(p2)
    if i%10000 ==0:
        print(i)
n_large = len(select_list)
print("第一遍做完了,入队%d个节点"%len(connect_set))
original_set = len(connect_set)
largest_graph = all_array[select_list]
left_array = all_array[left_list]
n_large_new = 0

while n_large !=n_large_new:
    n=2
    select_list = []
    left_list = []
    for i in range(len(left_array) - 1):
        n_large = n_large_new
        p1, p2 = tuple(left_array[i])
        if p1 in connect_set or p2 in connect_set:
            select_list.append(i)
        else:
            left_list.append(i)
        connect_set.add(p1)
        connect_set.add(p2)
        if i % 10000 == 0:
            print(i)
    largest_graph=np.vstack((largest_graph,left_array[select_list]))
    left_array = left_array[left_list]
    n_large_new = n_large + len(select_list)
    print("第%d遍做完了，入队%d个节点"%(n,len(connect_set)-original_set))
    n+=1

largest_graph = pd.DataFrame(largest_graph)
small_graph = pd.DataFrame(left_array)
largest_graph.to_csv("C:\\Users\\mengboyu\\Desktop\\我的坚果云\\社交网络挖掘\\final-pj\\zhihu\\寻找最大联通图\\largest.csv")
small_graph.to_csv("C:\\Users\\mengboyu\\Desktop\\我的坚果云\\社交网络挖掘\\final-pj\\zhihu\\寻找最大联通图\\left.csv")