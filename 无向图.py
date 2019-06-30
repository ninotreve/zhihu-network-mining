'''find the largest connect graph'''
import pandas as pd
import numpy as np

df = pd.read_csv('C:\\Users\\mengboyu\\Desktop\\我的坚果云\\社交网络挖掘\\final-pj\\zhihu\\边预测\\ke_leader.csv')#改成文件名字
connect_set = set()
point_set = set()
select_list = []
left_list = []
all_array = np.array(df)
for i in all_array.tolist():
    connect_set.add(tuple(i))
print(len(all_array))
for i in range(len(all_array)-1):
    p1, p2 = tuple(all_array[i])
    if (p2,p1) in connect_set:
        select_list.append(i)
        point_set.add(p1)
        point_set.add(p2)
    if i%10000 ==0:
        print(i)
n_large = len(select_list)
print("入队%d个边"%len(select_list))
print("入队%d个点"%len(point_set))
connect_graph = pd.DataFrame(all_array[select_list])
connect_graph.to_csv("C:\\Users\\mengboyu\\Desktop\\我的坚果云\\社交网络挖掘\\final-pj\\zhihu\\边预测\\ke_leader.csv")
