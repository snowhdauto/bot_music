import shelve
from SQL import SQLighter
from random import shuffle
import config

storagename="botStorage.db"

def IsTest(chatid):
        with shelve.open(storagename) as storage:
                try:
                        return storage[str(chatid)]!=None
                except KeyError:
                        return False

def set_user_test(chatid,userid):
	li=SQLighter().getListQuestions()
	with shelve.open(storagename) as storage:
		storage[str(chatid)]={
                	"user":[userid,chatid],
                        "list":li,
                        "quest":li[0][1],
                        "correct":li[0][2],
                        "current":0,
                }
		dic={
                        'quest':li[0][1],
                        'list':li[0][2].split(";")+li[0][3].split(";")
                }
		shuffle(dic['list'])
		return dic

def nextQuestion(chatid):
        with shelve.open(storagename) as storage:
                cur=storage[str(chatid)]['current']+1
                try:
                        li=storage[str(chatid)]['list'][cur]
                        
                        dic={
                                "user":storage[str(chatid)]['user'],
                                "list":storage[str(chatid)]['list'],
                                "current":cur,
                                'quest':li[1],
                                'correct':li[2]
                        }
                        storage[str(chatid)]=dic
                        
                        dic={
                                'quest':li[1],
                                'list':li[2].split(";")+li[3].split(";")
                        }
                        shuffle(dic['list'])
                        return dic
                        
                except IndexError:
                       
                        if getMember(storage[str(chatid)]['user'][0]):
                                SQLighter().AddMember(storage[str(chatid)]['user'][0],storage[str(chatid)]['user'][1])
                        finish_user_test(chatid)
                        return {
                                'quest':"Тест пройден!",
                                'list': None
                        }                         

def getMember(userid): 
        if (config.bot.get_chat_member(config.groupId,userid).status == 'left'):
                return True
        else:
                return False

def finish_user_test(chatid):
    with shelve.open(storagename) as storage:
        del storage[str(chatid)]

def get_answer_for_user(chatid):
    with shelve.open(storagename) as storage:
        try:
            return storage[str(chatid)]['correct'].split(";")
        except KeyError:
            return None