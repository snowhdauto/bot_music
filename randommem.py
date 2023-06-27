import random 
import SQL

def getRandMem():
    li=SQL.SQLighter().GetMemberList()
    if (len(li)>0):
        random.shuffle(li)
        return li[0]
    else:
        return None