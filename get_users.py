#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 13:37:44 2017

@author: uba
"""

import pandas as pd 
from datetime import datetime

data = pd.read_csv('/home/uba/Downloads/logs/wac_1AC1_20160422_0082.log',delimiter=" ",skiprows=1,header=None)
data.columns = ["timestamp","time_taken","c_ip","filesize","s_ip","s_port","sc_status",
                "sc_bytes","cs_method","cs_uri_stem","_","rs_duration","rs_bytes",
                "c_referrer","c_user_agent","customer_id","x_ec_custom_1","None"]
                
records = [512, 129, 4, 6, 7, 523, 396, 399, 786, 280, 920, 666, 668, 423, 297, 170, 814, 47, 434, 311, 185, 442, 705, 197, 838, 841, 458, 588, 336, 85, 470, 349, 606, 865, 101, 747, 876, 110, 242, 628, 374, 887, 376, 379]

for r in records:
    #print(data[['c_ip','c_user_agent','x_ec_custom_1']].loc[r])
    print(data['c_ip'].loc[r])
#    print(datetime.fromtimestamp(data['timestamp'].loc[r]))
#    print(data['c_user_agent'].loc[r])
#    print(data['x_ec_custom_1'].loc[r])
    print('---------------------------------------------')
    #print(data[['c_ip','x_ec_custom_1']].loc[r].values)