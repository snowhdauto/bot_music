from telebot import types
import state
import config
from SQL import SQLighter
import DataProcessor
import Storage
import randommem
import time

'''@config.bot.message_handler(func=lambda message: True, content_types=['text'])
def test2(message):
        print (message)'''

def ButAnswGen(quest):
        if quest['list']!= None:
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                DataProcessor.GetRows(markup,quest['list'],2)
                return markup
        #else:
                #keyboard = types.InlineKeyboardMarkup()
                #keyboard.add(types.InlineKeyboardButton(text="Перейти в группу", url=bot.export_chat_invite_link(config.groupId)))
                #return keyboard

def getAdmins():
        li=[]
        for i in config.bot.get_chat_administrators(config.groupId):
                li.append(i.user.id)
        return li

#RANDOM
@config.bot.message_handler(func=lambda message:message.from_user.id in getAdmins() and message.chat.type=='private',commands=['random'])
def rendomMem(message):
	mem=randommem.getRandMem()
	if mem != None:
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(types.InlineKeyboardButton(text="Перейти в группу", url=config.bot.export_chat_invite_link(config.groupId)))
                config.bot.send_message(mem[0],"Поздравляю вы были удостоены чести вступить в группу.",reply_markup=keyboard)
                SQLighter().DelMember(mem[0])
	else:
		config.bot.send_message(message.chat.id, 'На данный момент, недостаточно человек прошло тестирование, чтобы выбрать из списка.')

#START

@config.bot.message_handler(func=lambda message: message.chat.type=='private',commands=['start'])
def start(message):
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add("Пройти тест")
        config.bot.send_message(message.chat.id, 'Чтобы пройти тест и поучаствовать в розыгрыше нажмите на "Пройти тест"!', reply_markup=markup)
        if message.from_user.id in getAdmins():
                state.retunMenu(message.chat.id)
#DELALL

def delallController(message):
        SQLighter().delall()
        config.bot.send_message(message.chat.id, 'Все вопросы удалены!')
        state.set_state(message.chat.id, config.States.S_MENU.value)

#MENU
menuOpt=["Добавить вопрос","Удалить вопрос","Удалить все вопросы"]
def menu(idchat):
        config.bot.send_message(idchat, "Выберите действие:", reply_markup=ButAnswGen({'list':menuOpt}))
        state.set_state(idchat, config.States.S_MENU.value)

@config.bot.message_handler(func=lambda message:message.from_user.id in getAdmins() and message.chat.type=='private', commands=['menu'])
def controller(message):
        menu(message.chat.id)

@config.bot.message_handler(func=lambda message: state.get_current_state(message.chat.id) == config.States.S_MENU.value and message.chat.type=='private' and message.from_user.id in getAdmins() and message.text in menuOpt )
def firstReactions(message):
        if message.text==menuOpt[0]:
                config.bot.send_message(message.chat.id, "Для начала введите сам вопрос.",reply_markup=types.ReplyKeyboardRemove())
                state.set_state(message.chat.id, config.AddQuest.S_Quest.value)
        if message.text==menuOpt[1]:
                state.set_state(message.chat.id, config.DelQuest.S_QuestList.value)
                QuestList(message.chat.id)
        if message.text==menuOpt[2]:
                delallController(message)

#ADDQUESTION

@config.bot.message_handler(func=lambda message: state.get_current_state(message.chat.id) == config.AddQuest.S_Quest.value and message.chat.type=='private' and message.from_user.id in getAdmins())
def AddQuest(message):
        if message.text is not None:
                state.set_addquest_chdatastate(message.chat.id,"Quest",message.text)
                config.bot.send_message(message.chat.id, "Отлично, теперь введите правильный ответ на ваш вопрос. Если ответов больше одного, то пречислите их через точку с зяпятой ( ; ).")
                state.set_state(message.chat.id, config.AddQuest.S_CAnswers.value)
        else:
                config.bot.send_message(message.chat.id, "Странно, но вопрос отсутсвует, попробуйте ещё раз:")

@config.bot.message_handler(func=lambda message: state.get_current_state(message.chat.id) == config.AddQuest.S_CAnswers.value and message.chat.type=='private' and message.from_user.id in getAdmins())
def AddСAnsw(message):
        if message.text is not None:
                state.set_addquest_chdatastate(message.chat.id,"CAnsw",message.text)
                config.bot.send_message(message.chat.id, "Отлично, теперь введите неверный ответ на ваш вопрос. Если ответов больше одного, то пречислите их через точку с зяпятой ( ; ).")
                state.set_state(message.chat.id, config.AddQuest.S_WAnswers.value)
        else:
                config.bot.send_message(message.chat.id, "Странно, но правильный ответ отсутсвует, попробуйте ещё раз:")

@config.bot.message_handler(func=lambda message: state.get_current_state(message.chat.id) == config.AddQuest.S_WAnswers.value and message.chat.type=='private' and message.from_user.id in getAdmins())
def AddWAnsw(message):
        if message.text is not None:
                state.set_addquest_chdatastate(message.chat.id,"WAnsw",message.text)
                state.set_state(message.chat.id, config.AddQuest.S_WAnswers.value)
                SQLighter().AddQuest(state.get_current_dic(message.chat.id))
                config.bot.send_message(message.chat.id, "Вопрос был добавлен.")
                menu(message.chat.id)
                state.retunMenu(message.chat.id)
        else:
                config.bot.send_message(message.chat.id, "Странно, но неверный ответ отсутсвует, попробуйте ещё раз:")

#DELQUESTION

def QuestList(chatid):
        keyboard = types.InlineKeyboardMarkup()
        for i in SQLighter().getListQuestions():
                keyboard.add(types.InlineKeyboardButton(text=i[1],callback_data=i[0]))
        config.bot.send_message(chatid, "Выберите вопрос для удаления.",reply_markup=keyboard)

@config.bot.callback_query_handler(func=lambda call: state.get_current_state(call.message.chat.id) == config.DelQuest.S_QuestList.value and call.message.chat.type=='private' and call.from_user.id in getAdmins())
def callback_inline(call):
        SQLighter().DelQuest(call.data)
        config.bot.send_message(call.message.chat.id, "Вопрос был удалён!")
        menu(call.message.chat.id)
        state.retunMenu(call.message.chat.id)

#TEST

@config.bot.message_handler(func=lambda message: message.content_type=="text" and message.chat.type=='private' and message.text=="Пройти тест", content_types=['text'])
def test(message):
        quest=Storage.set_user_test(message.chat.id,message.from_user.id)        
        config.bot.send_message(message.chat.id, quest['quest'], reply_markup=ButAnswGen(quest))

def checkanswer(message):
        for i in Storage.get_answer_for_user(message.chat.id):
                if i.strip() == message.text:
                        return True
        return False

@config.bot.message_handler(func=lambda message: message.content_type=="text" and message.chat.type=='private' and Storage.IsTest(message.chat.id), content_types=['text'])
def test1(message):
        
        try:
                if checkanswer(message):
                        config.bot.send_message(message.chat.id, "Верно!")
                                
                        quest = Storage.nextQuestion(message.chat.id)
                        config.bot.send_message(message.chat.id, quest['quest'], reply_markup=ButAnswGen(quest))
                        
                else:
                        Storage.finish_user_test(message.chat.id)
                        quest={
                                'quest':"Неправильно! Вы не прошли тест!\nНажмите на кнопку 'Пройти тест', чтобы попробовать ещё раз.",
                                'list':['Пройти тест']
                        }
                        config.bot.send_message(message.chat.id, quest['quest'], reply_markup=ButAnswGen(quest))
        except TypeError:
                pass




if __name__ == '__main__':
	print ('start')
	config.bot.polling(none_stop=True, interval=0)
