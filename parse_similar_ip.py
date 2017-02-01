#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 16:35:54 2017

@author: uba
"""

import pandas as pd
import re
from datetime import datetime
import numpy as np
import networkx as nx
from itertools import combinations
import urllib.request
import multiprocessing as mp
import time


start = time.time()
data = pd.read_csv('/home/uba/Downloads/logs/wac_1AC1_20160422_0082.log', delimiter=" ", skiprows=1,header=None)
#data = pd.read_csv('/home/uba/Downloads/logs/small.log', delimiter=" ", skiprows=1,header=None)
data.columns = ["timestamp","time_taken","c_ip","filesize","s_ip",
                "s_port","sc_status","sc_bytes","cs_method","cs_uri_stem",
                "_","rs_duration","rs_bytes","c_referrer","c_user_agent",
                "customer_id","x_ec_custom_1","None"]
                
unique_users = list(data.groupby(["c_ip"])) #list of tuples, inside tuple -> (ip,dataframe of users with that ip)
print(len(unique_users))
#for user in unique_users:
#    ip = user[0]
#    #print(ip)
#    response = urllib.request.urlopen("http://api.ipinfodb.com/v3/ip-city/?key=e0b49b58117d328808430443277e6ed2f0497aad602018827620571c7accd12c&ip="+str(ip)).read()
#    print(response)

#user = unique_users[509][1]
#for each in user["x_ec_custom_1"].values:
#    print(each)

#print(data.loc[0])
'''print(data.loc[9466]["timestamp"])
print(data.loc[9466]["c_user_agent"])
print(data.loc[9466]["x_ec_custom_1"])
print((re.search("(?P<url>https?://[^\s]+)", data.loc[9466]["x_ec_custom_1"]).group("url")).split('/')[2])

print(data.loc[9388]["timestamp"])
print(data.loc[9388]["c_user_agent"])
print(data.loc[9388]["x_ec_custom_1"])
print((re.search("(?P<url>https?://[^\s]+)", data.loc[9388]["x_ec_custom_1"]).group("url")).split('/')[2])'''

def similarity_score(a,b):
    score = [0]*3
    if abs(a["timestamp"] - b["timestamp"]) <= 300:
        score[0] = 1
    if a["c_user_agent"] == b["c_user_agent"]:
        score[1] = 1
    try:
        site_a = (re.search("(?P<url>https?://[^\s]+)", a["x_ec_custom_1"]).group("url")).split('/')[2]
    except:
        site_a = None
    try:
        site_b = (re.search("(?P<url>https?://[^\s]+)", b["x_ec_custom_1"]).group("url")).split('/')[2]
    except:
        site_b = None
    if site_a == site_b:
        score[2] = 1
    weights = [1,2,3]
    return sum(np.array(score)*np.array(weights))/6

#print(similarity_score(data.loc[9466],data.loc[9388]))


#print(unique_users[0][1].index.values)

############################### main process ##################################

global G 
G = nx.Graph()
G.add_nodes_from(list(range(len(data))))

for user in unique_users:
    members = user[1].index.values
    #print(members)
    #print(list(combinations(members,2)))
    G.add_edges_from(list(combinations(members,2)))
    

#all_pairs = set()
#for i in range(len(data)):
#    for j in range(i+1,len(data)):
#        if i != j:
#            if data.loc[i]['c_ip'] != data.loc[j]['c_ip']:
#                all_pairs.add(tuple(sorted([i,j])))
                
all_pairs = list(combinations(range(len(data)),2))            
print(len(all_pairs))

global scores
scores = set()
#for a,b in all_pairs:
#    score = similarity_score(data.loc[a],data.loc[b])
#    scores.add(score)
#    if score == 1.0:
#        G.add_edge(a,b)

def run_process(p):
    for a,b in p:
        score = similarity_score(data.loc[a],data.loc[b])
        scores.add(score)
        if score == 1.0:
            G.add_edge(a,b)
            
def run_process2(pair):
    score = similarity_score(data.loc[pair[0]],data.loc[pair[1]])
    if score == 1.0:
        return 1
    else:
        return 0


#sub_lists = []
#n = 4
#for i in range(0,len(list(all_pairs)),int(len(list(all_pairs))/n)):
#    sub_lists.append(list(all_pairs)[i:i+int(len(list(all_pairs))/n)])
#
#jobs = []
#for i in range(n):
#    p = mp.Process(target=run_process(sub_lists[i]))
#    jobs.append(p)
#
#for j in jobs:
#    j.start()
#
#for j in jobs:
#    j.join()

p = mp.Pool(4)
res = p.map(run_process2,list(all_pairs))

for i in range(len(res)):
    if res[i] == 1:
        G.add_edge(list(all_pairs)[i][0],list(all_pairs)[i][1])
   
#for pos, item in enumerate(res):
#    if item == 1:
#        G.add_edge(list(all_pairs)[pos][0],list(all_pairs)[pos][1])
        
print(scores)
    
users = list(nx.connected_components(G))
print(users)
print(len(users))

print(time.time()-start)

###############################################################################

#print(len(data))

'''all_pairs = set()
for i in range(len(data)):
    for j in range(i+1,len(data)):
        if i != j:
            all_pairs.add(tuple(sorted([i,j])))
#            if tuple(sorted([i,j])) not in all_pairs:
#                all_pairs.append(tuple(sorted([i,j])))
                
print(len(all_pairs))'''

#            if similarity_score(data.loc[i],data.loc[j]) == 1.0:
#                G.add_edge(i,j)
                
#print(data.loc[9686])

'''    
for user in unique_users:
    for each in user[1]["x_ec_custom_1"].values:
        try:
            #print(each[5:])
            #print(re.search("(?P<url>https?://[^\s]+)", each).group("url"))
            #print(re.search("(?P<url>https?://[^\s]+)", each).group("url"))
            url = re.search("(?P<url>https?://[^\s]+)", each).group("url")
            print(url.split('/')[2])
        except:
            pass
        #print(each[5:])'''
'''        
for user in unique_users:
    for each in user[1]["timestamp"].values:
        print(each)'''

'''print(data["timestamp"].min())
print(datetime.fromtimestamp(data["timestamp"].min()))
print(data["timestamp"].max())
print(datetime.fromtimestamp(data["timestamp"].max()))'''

'''                             
s = data.groupby(["c_ip"]).size().values
print(sorted(s))'''