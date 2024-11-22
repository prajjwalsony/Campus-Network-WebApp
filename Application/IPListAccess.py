import pandas as pd
import random as rd


def getIP(id):
    df = pd.read_csv("ipList.csv")
    if len(df)==0:
        return "NULL"
    return (df.loc[df['id'] == int(id), 'ip']).iloc[0]

def addIP(id, ip, name=str('contact'+str(rd.randint(1000,9999)))):
    id=int(id)
    df = pd.read_csv("ipList.csv")
    if id in df['id'].values:
        df.loc[df['id'] == id, 'ip'] = ip
        df.to_csv('ipList.csv', index=False)
        return
    new_row = {'id': str(id), 'name' : name, 'ip': ip, 'message':"[]"}
    df = df._append(new_row, ignore_index=True)
    df.to_csv('ipList.csv', index=False)

def getMessage(id):
    df = pd.read_csv("ipList.csv")
    if len(df)==0:
        return "NULL"
    return (df.loc[df['id'] == int(id), 'message']).iloc[0]

def getName(id):
    df = pd.read_csv("ipList.csv")
    if len(df)==0:
        return "NULL"
    return (df.loc[df['id'] == int(id), 'name']).iloc[0]

def addMessage(id, message, person): #person is sender or receiver
    id=int(id)
    df = pd.read_csv("ipList.csv")
    if id in df['id'].values:
        lst=eval((df.loc[df['id'] == id, 'message'].iloc[0]))
        if person == "S":
            lst.append("@S:"+str(message))
        else:
            lst.append("@R:"+str(message))
        df.loc[df['id'] == id, 'message'] = str(lst)
        df.to_csv('ipList.csv', index=False)

def getNameIdList():
    df = pd.read_csv("ipList.csv")
    return (df['name']), df['id']
    

# print(getIP(1))
# print(pd.read_csv("ipList.csv")) 
