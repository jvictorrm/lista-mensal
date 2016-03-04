import telebot
import configparser
# import datetime
from control_bills import *

"""
Setup the bot
"""

# get token from '.ini' file
config = configparser.ConfigParser()
config.read('telebot.ini')
bot = telebot.TeleBot(config['default']['token'])

dbjson = load_database() # get 'database' from json file
yearmonth = ''.join([x for x in dbjson.keys()])  # get 'yearmonth' key (YYYYMM) from json


# Command '/list' to show all bills
@bot.message_handler(commands=['list'])
def send_bills(message):
    bot.send_message(message.chat.id, show_bills(dbjson, yearmonth), parse_mode='HTML')


# Command '/keys' to show all bills key's
@bot.message_handler(commands=['keys'])
def send_bills_keys(message):
    bot.send_message(message.chat.id, show_bills_keys(dbjson, yearmonth), parse_mode='HTML')


# Command '/new' to create a new bill
@bot.message_handler(commands=['new'])
def create_new_bill(message):
    msg = """
Informe a nova conta no formato: <b>key|descr|value|status*|pay_day*</b>
<i>(*) Campos não obrigatórios</i>
    """
    resp = bot.send_message(message.chat.id, msg, parse_mode='HTML')
    bot.register_next_step_handler(resp, get_new_bill)


# create a new bill from telegram bot
def get_new_bill(message):
    key, descr, value, status, pay_day = message.text.split('|')
    value = float(value) if is_number(value) else value
    status = bool(status)
    print(key, descr, value, status, pay_day)
    msg = "Nova conta inserida: <b>{}</b>".format(key)
    bot.send_message(message.chat.id, msg, parse_mode='HTML')


# Command '/alt' to modify a created bill
@bot.message_handler(commands=['alt'])
def modify_bill(message):
    msg = "Altere a conta desejada no formato: <b>key|attr|new_value</b>"
    resp = bot.send_message(message.chat.id, msg, parse_mode='HTML')
    bot.register_next_step_handler(resp, get_modified_bill)


# modify a created bill from telegram bot
def get_modified_bill(message):
    key, attr, new_value = message.text.split('|')
    new_value = float(new_value) if is_number(new_value) else new_value
    print(key, attr, new_value)
    msg = "<b>{0}</b> da conta <b>{1}</b> alterada!".format(attr.capitalize(), key)
    bot.send_message(message.chat.id, msg, parse_mode='HTML')


# Command '/del' to remove a created bill
@bot.message_handler(commands=['del'])
def remove_bill(message):
    msg = "Delete a conta desejada no formato: <b>key</b>"
    resp = bot.send_message(message.chat.id, msg, parse_mode='HTML')
    bot.register_next_step_handler(resp, get_deleted_bill)


# delete a created bill from telegram bot
def get_deleted_bill(message):
    key = message.text
    msg = "Conta <b>{0}</b> removida!".format(key)
    print(key)
    bot.send_message(message.chat.id, msg, parse_mode='HTML')


# create a new bill
'''new_bill(database=dbjson,
         yearmonth=yearmonth,
         key='teste',
         descr='testando namoral',
         value=499,
         status=True)'''

# alter a created bill
'''alter_bill(database=dbjson,
           yearmonth=yearmonth,
           key='teste',
           attr='descr',
           new_value='tEstar alteracao')'''

# delete a created bill
'''delete_bill(dbjson, yearmonth, 'teste')'''

# save_database(dbjson)
# dbjson = load_database()

print('Wikibills em atividade...')
bot.polling()
