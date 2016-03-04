# coding: utf-8
import telebot
import configparser
# import datetime
from control_bills import *

"""
Setup the bot
"""

# get token from '.ini' file
config = configparser.ConfigParser()
config.read('project.ini')
bot = telebot.TeleBot(config['telegram']['token'])


# Command '/list' to show all bills
@bot.message_handler(commands=['list'])
def send_bills(message):
    dbjson = load_database()
    yearmonth = ''.join([x for x in dbjson.keys()])
    bot.send_message(message.chat.id, show_bills(dbjson, yearmonth), parse_mode='HTML')


# Command '/keys' to show all bills key's
@bot.message_handler(commands=['keys'])
def send_bills_keys(message):
    dbjson = load_database()
    yearmonth = ''.join([x for x in dbjson.keys()])
    bot.send_message(message.chat.id, show_bills_keys(dbjson, yearmonth), parse_mode='HTML')


# Command '/wiki' to show all commands
@bot.message_handler(commands=['wiki'])
def send_help_cmds(message):
    bot.send_message(message.chat.id, show_help_cmds(), parse_mode='HTML')


# Command '/pay' to show all commands
@bot.message_handler(commands=['pay'])
def pay_bill(message):
    msg = """Informe a conta a ser paga no formato: <b>key</b>

<b>key</b> - Chave da conta
    """
    resp = bot.send_message(message.chat.id, msg, parse_mode='HTML')
    bot.register_next_step_handler(resp, get_paid_bill)


# pay a bill from telegram bot
def get_paid_bill(message):
    dbjson = load_database()
    yearmonth = ''.join([x for x in dbjson.keys()])

    key = message.text.lower()
    msg = "Conta <b>{}</b> paga!".format(key)
    change_status_bill(dbjson, yearmonth, key, True)
    bot.send_message(message.chat.id, msg, parse_mode='HTML')


# Command '/owe' to show all commands
@bot.message_handler(commands=['owe'])
def owe_bill(message):
    msg = """Informe a conta a ser devida no formato: <b>key</b>

<b>key</b> - Chave da conta
    """
    resp = bot.send_message(message.chat.id, msg, parse_mode='HTML')
    bot.register_next_step_handler(resp, get_owed_bill)


# to owe a bill from telegram bot
def get_owed_bill(message):
    dbjson = load_database()
    yearmonth = ''.join([x for x in dbjson.keys()])

    key = message.text.lower()
    msg = "Conta <b>{}</b> devida!".format(key)
    change_status_bill(dbjson, yearmonth, key, False)
    bot.send_message(message.chat.id, msg, parse_mode='HTML')


# Command '/detail' to show all attributes from bill
@bot.message_handler(commands=['detail'])
def pay_bill(message):
    msg = """Informe a conta a ser detalhada no formato: <b>key</b>

<b>key</b> - Chave da conta
    """
    resp = bot.send_message(message.chat.id, msg, parse_mode='HTML')
    bot.register_next_step_handler(resp, get_detailed_bill)


# to detail a bill from telegram bot
def get_detailed_bill(message):
    dbjson = load_database()
    yearmonth = ''.join([x for x in dbjson.keys()])
    key = message.text.lower()

    msg = """Informações da chave <b>{0}</b>

Descr....: <b>{1}</b>
Valor....: <b>{2:6.2f}</b>
Dt. Venc.: <b>{3}</b>
Status...: <b>{4}</b>
    """.format(key,
               dbjson[yearmonth]['expense'][key]['descr'][0:13],
               dbjson[yearmonth]['expense'][key]['value'],
               dbjson[yearmonth]['expense'][key]['pay_day'],
               'Pago' if dbjson[yearmonth]['expense'][key]['status'] else 'Devendo')

    bot.send_message(message.chat.id, msg, parse_mode='HTML')


# Command '/turn_month' to turn the month in activity
@bot.message_handler(commands=['turn_month'])
def turn_month(message):
    msg = "Envie <b>Sim</b> para confirmar ou <b>Não</b> para cancelar a virada do mês:"

    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
    keyboard.row('Sim')
    keyboard.row('Não')

    resp = bot.send_message(message.chat.id, msg, parse_mode='HTML', reply_markup=keyboard)
    bot.register_next_step_handler(resp, get_resp_turn_month)


# to turn the month in activity from telegram bot
def get_resp_turn_month(message):
    dbjson = load_database()
    yearmonth = ''.join([x for x in dbjson.keys()])

    resp = message.text.capitalize()

    if resp not in ['Sim', 'S']:
        bot.send_message(message.chat.id, "Operação cancelada!")
    else:
        change_month_activity(dbjson, yearmonth)
        bot.send_message(message.chat.id, "Operação realizada!")


# Command '/new' to create a new bill
@bot.message_handler(commands=['new'])
def create_new_bill(message):
    msg = """
Informe a nova conta no formato: <b>key|descr|value|status|pay_day</b>

<b>key</b> - Chave da conta
<b>descr</b> - Descrição da conta
<b>value</b> - Valor da conta
<b>status*</b> - Status da conta (Deixar vazio para DEVENDO)
<b>pay_day*</b> - Dt. de Venc. da conta

<i>(*) Campos não obrigatórios</i>
    """
    resp = bot.send_message(message.chat.id, msg, parse_mode='HTML')
    bot.register_next_step_handler(resp, get_new_bill)


# create a new bill from telegram bot
def get_new_bill(message):
    dbjson = load_database()
    yearmonth = ''.join([x for x in dbjson.keys()])

    key, descr, value, status, pay_day = message.text.split('|')

    new_bill(database=dbjson,
             yearmonth=yearmonth,
             key=key.lower(),
             descr=descr,
             value=float(value),
             status=bool(status))
    msg = "Nova conta inserida: <b>{}</b>".format(key)
    bot.send_message(message.chat.id, msg, parse_mode='HTML')


# Command '/alt' to modify a created bill
@bot.message_handler(commands=['alt'])
def modify_bill(message):
    msg = """Altere a conta desejada no formato: <b>key|attr|new_value</b>

<b>key</b> - Chave da conta
<b>attr</b> - Atributo da conta
<b>new_value</b> - Novo valor para o atrib. da conta
    """
    resp = bot.send_message(message.chat.id, msg, parse_mode='HTML')
    bot.register_next_step_handler(resp, get_modified_bill)


# modify a created bill from telegram bot
def get_modified_bill(message):
    dbjson = load_database()
    yearmonth = ''.join([x for x in dbjson.keys()])

    key, attr, new_value = message.text.split('|')
    new_value = float(new_value) if is_number(new_value) else new_value

    alter_bill(database=dbjson,
               yearmonth=yearmonth,
               key=key.lower(),
               attr=attr,
               new_value=new_value)
    msg = "<b>{0}</b> da conta <b>{1}</b> alterada!".format(attr.capitalize(), key)
    bot.send_message(message.chat.id, msg, parse_mode='HTML')


# Command '/del' to remove a created bill
@bot.message_handler(commands=['del'])
def remove_bill(message):
    msg = """Delete a conta desejada no formato: <b>key</b>

<b>key</b> - Chave da conta
"""
    resp = bot.send_message(message.chat.id, msg, parse_mode='HTML')
    bot.register_next_step_handler(resp, get_deleted_bill)


# delete a created bill from telegram bot
def get_deleted_bill(message):
    dbjson = load_database()
    yearmonth = ''.join([x for x in dbjson.keys()])

    key = message.text.lower()
    msg = "Conta <b>{0}</b> removida!".format(key)
    delete_bill(dbjson, yearmonth, key)
    bot.send_message(message.chat.id, msg, parse_mode='HTML')


print('Wikibills em atividade...')
bot.polling()
