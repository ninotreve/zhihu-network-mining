
# coding: utf-8

# In[1]:


import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from collections import Counter
from networkx import algorithms as algo
import jieba
import jieba.analyse


# In[2]:


class Clusters:
    def __init__(self, full_filepath, follow_filepath, leader_filepath):
        self.full = pd.read_csv(full_filepath)
        self.follow = pd.read_csv(follow_filepath)
        self.columns = ['badge_identity','badge_topics','business','headline','job_curr','job_prev','major_curr','major_prev']
        self.leader = pd.read_csv(leader_filepath, encoding='gb18030').set_index('url_token')
        
    def findBigClusters(self, n=10):
        '''找到包含至少n个结点的大类，并返回类的id'''
        count = self.full[['id','modularity_class']].groupby(['modularity_class']).count()
        print('共有',count.shape[0],'类。')
        big = count.loc[count['id'] > n,]
        print(big)
        return list(big.index)
    
    def generateClusterGraph(self, clusterid=None):
        '''生成clusterid的图，并写入csv'''
        if clusterid is None:
            cluster = self.full.loc[:,['url_token']]
        else:
            cluster = self.full.loc[self.full['modularity_class']==clusterid,['url_token']]
        cluster_from = cluster.set_index('url_token').join(self.follow.set_index('from_id')).reset_index().drop(
            ['id'], axis=1).rename(index=str, columns={"index": "from_id"})
        cluster_to = cluster.set_index('url_token').join(cluster_from.set_index('to_id'), how='inner').reset_index().rename(
            index=str, columns={"index": "to_id"})
        
        G = nx.DiGraph() # 有向图
        nodes = list(cluster['url_token'])
        edges = list(cluster_to[['from_id','to_id']].itertuples(index=False, name=None))
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)
        return G
    
    def displayGraphProperties(self, G):
        '''展示图的基本性质'''
        print('结点数：', len(G.nodes()))
        print('边数：', len(G.edges()))
        print('互粉边比例：', algo.reciprocity(G))
        print('是否是弱连通子图：', algo.components.is_weakly_connected(G))
        print('弱连通子图数量：', algo.components.number_weakly_connected_components(G))
        print('弱连通子图的大小：')
        components = list(algo.components.weakly_connected_components(G))
        len_components = [len(component) for component in components]
        count = Counter(len_components)
        print(count)
        
    def findBigVinG(self, G, n=10):
        '''返回n项列表，是前n入度的节点'''
        listE = sorted(dict(G.in_degree).items(), key=lambda d: d[1], reverse = True)[:n]
        return [i[0] for i in listE]
    
    def howManyBigV(self, G, lst):
        '''判断多少大V可以代表一社群'''
        '''lst must have bigv sorted'''
        node_list = []
        node_perc_list = []
        edge_perc_list = []
        for bigv in lst:
            node_list.append(bigv)
            node_list.extend(G.successors(bigv))
            node_list.extend(G.predecessors(bigv))
            node_list = list(set(node_list))
            G_sub = nx.subgraph(G, node_list)
            node_perc = len(G_sub.nodes())/len(G.nodes())
            edge_perc = len(G_sub.edges())/len(G.edges())
            node_perc_list.append(node_perc)
            edge_perc_list.append(edge_perc)
        plt.plot(range(1,len(node_perc_list)+1),node_perc_list, 'bo-',label='node_percentage')
        plt.plot(range(1,len(edge_perc_list)+1),edge_perc_list, 'ro-',label='edge_percentage')
        plt.legend()
        plt.show()
        
    def displayBigVGraph(self, G, listV):
        '''用networkx画出代表们之间的关键图'''
        G_sub = nx.subgraph(G, listV)
        nx.draw(G_sub, with_labels=True)
        plt.show()
        
    def extractLabels(self, listV):
        '''从代表的更多信息中获取标签+tf-idf值'''
        rep = self.leader.loc[listV, self.columns]
        info_string = ','.join([str(j) for i in rep.iteritems() for j in i[1] if j is not np.nan])
        return jieba.analyse.extract_tags(info_string, topK=10, withWeight=True, allowPOS=())
    
    def urltoken2username(self, url_token):
        '''完成url_token到username的转换'''
        return self.leader.loc[url_token, 'username']


# In[3]:


ke_full = 'ke_full.csv'
ke_follow = 'ke_follow.csv'
ke_leader = 'ke_leader_info.csv'


# In[4]:


ke = Clusters(ke_full, ke_follow, ke_leader)


# In[5]:


xinli_full = 'xinli_full.csv'
xinli_follow = 'xinli_follow.csv'
xinli_leader = 'xinli_leader_info.csv'


# In[6]:


xinli = Clusters(xinli_full, xinli_follow, xinli_leader)


# In[7]:


c_ke = ke.findBigClusters()


# In[8]:


c_xinli = xinli.findBigClusters()


# In[9]:


c_xinli


# 5/6/15/22/25/27是大类。

# In[10]:


len(c_ke)


# In[11]:


clusterdict_ke = dict()
clusterdict_xinli = dict()


# 对于36氪有23个大类.

# In[12]:


for i in c_ke:
    i = int(i)
    print('-----------第',i,'类----------------')
    G = ke.generateClusterGraph(i)
    ke.displayGraphProperties(G)
    clusterdict_ke[i] = ke.findBigVinG(G,20)
    ke.howManyBigV(G, clusterdict_ke[i])
    j = int(input('输入拐点：'))
    clusterdict_ke[i] = clusterdict_ke[i][:j]
    bigV = []
    for token in clusterdict_ke[i]:
        try:
            bigV.append(ke.urltoken2username(token))
        except:
            continue
    print(bigV)
    labels = ke.extractLabels(clusterdict_ke[i])
    print([i[0] for i in labels])


# In[13]:


for i in c_xinli:
    i = int(i)
    print('-----------第',i,'类----------------')
    G = xinli.generateClusterGraph(i)
    xinli.displayGraphProperties(G)
    clusterdict_xinli[i] = xinli.findBigVinG(G,20)
    xinli.howManyBigV(G, clusterdict_xinli[i])
    j = int(input('输入拐点：'))
    clusterdict_xinli[i] = clusterdict_xinli[i][:j]
    bigV = []
    for token in clusterdict_xinli[i]:
        try:
            bigV.append(xinli.urltoken2username(token))
        except:
            continue
    print(bigV)
    labels = xinli.extractLabels(clusterdict_xinli[i])
    print([i[0] for i in labels])

