# -*- coding: UTF-8 -*-
import json
import os
import pandas as pd
import requests
# Filename : helloworld.py
# author by : www.runoob.com

# 该实例输出 Hello World!
#print("Hello World!")
#print("Hello World!")
appid=''
project=''
signature=''
url=''
nums=[]
with open('./notekey.conf', 'r') as f2:
    keys = f2.readlines()
# for i in range(0, len(keys)):
#     print i
# print keys[0]
# print keys[3]
for key in keys:
    # print key
    # print len(key.strip())
    if len(key.strip())>0:
        row=key.strip().split()
        if row[0]=='appid':
            appid = row[1]
        elif row[0]=='project':
            project=row[1]
        elif row[0]=='signature':
            signature=row[1]
        elif row[0]=='url':
            url=row[1]
        else:
            print row[0]

with open('./phnum.conf', 'r') as f1:
    nums = f1.readlines()

mon=dict()
mon['appid']=appid
mon['project']=project
mv=[]
mon['multi']=mv
mon['signature']=signature

data = pd.read_csv("./service.csv")
#print data
for index,row in data.iterrows():
    # print index
    # print row['serv']
    pid= os.popen('echo $(pidof '+row['serv']+')').read()
    #print pid.strip()
    if pid.strip()=='':
        vars1=dict()
        vars1['name']=row['serv'].strip()
        vars1['code']=1
        vars1['status']='进程挂了'
        submv = dict()
        for num in nums:
            if len(num.strip())>0:
                submv['to']=num.strip()
                submv['vars']=vars1
                mv.append(submv)
       #print mon
        jsondata=json.loads(json.dumps(mon, ensure_ascii=False, encoding="utf-8"))
        #分级报警
        if row['lvl']==0:
            res = requests.post(url,json=jsondata)
            #报警升级
            data.loc[index, 'lvl']=row['lvl']+1
            data.loc[index, 'cnt'] = 0
        elif row['lvl']==1:
            #报警等级阈值计数器，1级累计到5触发报警，报警后计数器清零
            data.loc[index, 'cnt']=row['cnt']+1
            if row['cnt']==5:
                res = requests.post(url, json=jsondata)
                data.loc[index, 'lvl'] = row['lvl'] + 1
                data.loc[index, 'cnt'] = 0
        elif row['lvl']==2:
            data.loc[index, 'cnt']=row['cnt']+1
            if row['cnt']==10:
                res = requests.post(url, json=jsondata)
                data.loc[index, 'lvl'] = row['lvl'] + 1
                data.loc[index, 'cnt'] = 0
        elif row['lvl']==3:
            data.loc[index, 'cnt']=row['cnt']+1
            if row['cnt']==30:
                res = requests.post(url, json=jsondata)
                data.loc[index, 'lvl'] = row['lvl'] + 1
                data.loc[index, 'cnt'] = 0
        elif row['lvl']==4:
            data.loc[index, 'cnt']=row['cnt']+1
            if row['cnt']==60:
                res = requests.post(url, json=jsondata)
                data.loc[index, 'lvl'] = row['lvl'] + 1
                data.loc[index, 'cnt'] = 0
        elif row['lvl']==5:
            data.loc[index, 'cnt']=row['cnt']+1
            if row['cnt']==180:
                res = requests.post(url, json=jsondata)
                data.loc[index, 'lvl'] = row['lvl'] + 1
                data.loc[index, 'cnt'] = 0
        else:
            data.loc[index, 'cnt']=row['cnt']+1
            if row['cnt']==60:
                res = requests.post(url, json=jsondata)
                data.loc[index, 'cnt'] = 0
    else:
        if row['lvl']>0:
            #进程恢复清空报警等级和计数
            data.loc[index, 'lvl']=0
            data.loc[index, 'cnt']=0

data.to_csv("./service.csv",index=0)

