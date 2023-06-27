import config
import shelve

db_file="statestorage.db"

def get_current_state(user_id):
    with shelve.open(db_file) as db:
        try:
            return db[str(user_id)]['state']
        except KeyError:  
            return {
                'state':config.States.S_MENU.value
            }

def get_current_dic(user_id):
    with shelve.open(db_file) as db:
        try:
            return db[str(user_id)]
        except KeyError:  
            return {
                'state':config.States.S_MENU.value
            }

def set_state(user_id, state):
   with shelve.open(db_file) as db:
        try:
            dic=db[str(user_id)]
            dic.update({'state':state})
            db[str(user_id)]=dic
            return True
        except:
            return False

def set_addquest_chdatastate(user_id,key,value):
    with shelve.open(db_file) as db:
        dic=db[str(user_id)]
        dic.update({key:value})
        db[str(user_id)]=dic
        return True

def retunMenu(user_id):
     with shelve.open(db_file) as db:
        db[str(user_id)]={
            'state':config.States.S_MENU.value
        }
        return True