import telebot
from telebot import apihelper

token="-"

proxy={'https':'-'}

groupId='-'

apihelper.proxy = proxy
bot = telebot.TeleBot(token)






#DEVELOPMENT ZONE 
from enum import Enum
class States(Enum):
    S_MENU = "M0"

class AddQuest(Enum):
    S_Quest="AQ0"
    S_CAnswers="AQ1"
    S_WAnswers="AQ2"

class DelQuest(Enum):
    S_QuestList="DQ0"
