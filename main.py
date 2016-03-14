# coding: utf-8
import configparser
import re

import telebot

from control_bills import *

"""
Setup the bot
"""

# get token from '.ini' file
config = configparser.ConfigParser()
config.read(os.path.dirname(os.path.abspath(__file__)) + '/project.ini')
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
    resp = re.search(r"^((\/pay){1} ([a-z]+(\-[a-z]+)*))$", message.text)
    if not resp:
        msg = "Comando com o <b>formato inválido</b>!\n" \
              "Formato correto: <b>/pay KEY</b>\n\n" \
              "<b>Operação cancelada</b>"
        bot.send_message(message.chat.id, msg, parse_mode='HTML')
        return

    key = resp.group(3)
    dbjson = load_database()
    yearmonth = ''.join([x for x in dbjson.keys()])

    msg = "Conta <b>{}</b> paga!".format(key)
    change_status_bill(dbjson, yearmonth, key, True)
    bot.send_message(message.chat.id, msg, parse_mode='HTML')


# Command '/owe' to show all commands
@bot.message_handler(commands=['owe'])
def owe_bill(message):
    resp = re.search(r"^((\/owe){1} ([a-z]+(\-[a-z]+)*))$", message.text)
    if not resp:
        msg = "Comando com o <b>formato inválido</b>!\n" \
              "Formato correto: <b>/owe KEY</b>\n\n" \
              "<b>Operação cancelada</b>"
        bot.send_message(message.chat.id, msg, parse_mode='HTML')
        return

    key = resp.group(3)
    dbjson = load_database()
    yearmonth = ''.join([x for x in dbjson.keys()])

    msg = "Conta <b>{}</b> em débito!".format(key)
    change_status_bill(dbjson, yearmonth, key, False)
    bot.send_message(message.chat.id, msg, parse_mode='HTML')


# Command '/detail' to show all attributes from bill
@bot.message_handler(commands=['detail'])
def detail_bill(message):
    resp = re.search(r"^((\/detail){1} ([a-z]+(\-[a-z]+)*))$", message.text)
    if not resp:
        msg = "Comando com o <b>formato inválido</b>!\n" \
              "Formato correto: <b>/detail KEY</b>\n\n" \
              "<b>Operação cancelada</b>"
        bot.send_message(message.chat.id, msg, parse_mode='HTML')
        return

    key = resp.group(3)
    dbjson = load_database()
    yearmonth = ''.join([x for x in dbjson.keys()])
    status = 'Pago' if dbjson[yearmonth]['expense'][key]['status'] else 'Devendo'

    msg_detail_templ.format(key,
               dbjson[yearmonth]['expense'][key]['descr'],
               dbjson[yearmonth]['expense'][key]['value'],
               dbjson[yearmonth]['expense'][key]['pay_day'],
               status)

    bot.send_message(message.chat.id, msg_detail_templ, parse_mode='HTML')


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
    if not message.text.capitalize() == 'Sim':
        msg = "<b>Operação cancelada</b>"
        bot.send_message(message.chat.id, msg, parse_mode='HTML')
        return

    dbjson = load_database()
    yearmonth = ''.join([x for x in dbjson.keys()])

    change_month_activity(dbjson, yearmonth)
    bot.send_message(message.chat.id, "<b>Operação realizada</b>", parse_mode='HTML')


# Command '/new' to create a new bill
@bot.message_handler(commands=['new'])
def create_new_bill(message):
    resp = bot.send_message(message.chat.id, msg_new_templ, parse_mode='HTML')
    bot.register_next_step_handler(resp, get_new_bill)


# create a new bill from telegram bot
def get_new_bill(message):
    pattern_new = r"^([a-z]+(\-[a-z]+)*)\|{1}" \
                  r"(\w+( \w+)*)\|{1}(\d+?(\.\d{2})?)\|{1}?([Pp])?\|{1}?(\d{2}\/\d{2}\/\d{4})?$"

    if not bool(re.search(pattern_new, message.text)):
        msg = "Entrada de Inserção com o <b>formato inválido</b>!\n\n" \
              "<b>Operação cancelada</b>"
        bot.send_message(message.chat.id, msg, parse_mode='HTML')
        return

    dbjson = load_database()
    yearmonth = ''.join([x for x in dbjson.keys()])

    key, descr, value, status, pay_day = message.text.split('|')

    new_bill(database=dbjson,
             yearmonth=yearmonth,
             key=key,
             descr=capitalize_str(descr),
             value=float(value),
             status=bool(status),
             pay_day=pay_day)

    msg = "Nova conta inserida: <b>{}</b>".format(key)
    bot.send_message(message.chat.id, msg, parse_mode='HTML')


# Command '/alt' to modify a created bill
@bot.message_handler(commands=['alt'])
def modify_bill(message):
    resp = bot.send_message(message.chat.id, msg_modify_templ, parse_mode='HTML')
    bot.register_next_step_handler(resp, get_modified_bill)


# modify a created bill from telegram bot
def get_modified_bill(message):
    pattern_alt = r"^([a-z]+(\-[a-z]+)*)\|([a-z]+(\_[a-z]+)*)\|(.*)$"

    if not bool(re.search(pattern_alt, message.text)):
        msg = "Entrada de Alteração com o <b>formato inválido</b>!\n\n" \
              "<b>Operação cancelada</b>"
        bot.send_message(message.chat.id, msg, parse_mode='HTML')
        return

    key, attr, new_value = message.text.split('|')

    if attr == 'descr':
        if not bool(re.search(r"^(\w+( \w+)*)$", new_value)):
            msg = "<b>Descrição</b> com o formato inválido!\n\n" \
                  "<b>Operação cancelada</b>"
            bot.send_message(message.chat.id, msg, parse_mode='HTML')
            return
        else:
            new_value = capitalize_str(new_value)
    elif attr == 'status':
        msg = "Para alterar o <b>Status</b> use os comandos <b>/pay ou /owe</b>!\n\n" \
              "<b>Operação cancelada</b>"
        bot.send_message(message.chat.id, msg, parse_mode='HTML')
        return
    elif attr == 'pay_day':
        if not bool(re.search(r"^(\d{2}/\d{2}/\d{4})$", new_value)) and not new_value == '':
            msg = "<b>Data de Vencimento</b> com o formato inválido!\n\n" \
                  "<b>Operação cancelada</b>"
            bot.send_message(message.chat.id, msg, parse_mode='HTML')
            return
    elif attr == 'value':
        if not bool(re.search(r"^(\d+?(\.\d{2})?)$", new_value)):
            msg = "<b>Valor da conta</b> com o formato inválido!\n\n" \
                  "<b>Operação cancelada</b>"
            bot.send_message(message.chat.id, msg, parse_mode='HTML')
            return
        else:
            new_value = float(new_value)

    dbjson = load_database()
    yearmonth = ''.join([x for x in dbjson.keys()])

    alter_bill(database=dbjson,
               yearmonth=yearmonth,
               key=key,
               attr=attr,
               new_value=new_value)

    msg = "<b>{}</b> da conta <b>{}</b> alterada!".format(attr.capitalize(), key)
    bot.send_message(message.chat.id, msg, parse_mode='HTML')


# Command '/del' to remove a created bill
@bot.message_handler(commands=['del'])
def remove_bill(message):
    resp = (re.search(r"^((\/del){1} ([a-z]+(\-[a-z]+)*))$", message.text))
    if not resp:
        msg = "Comando com o <b>formato inválido</b>!\n" \
              "Formato correto: <b>/del KEY</b>\n\n" \
              "<b>Operação cancelada</b>"
        bot.send_message(message.chat.id, msg, parse_mode='HTML')
        return

    key = resp.group(3)
    dbjson = load_database()
    yearmonth = ''.join([x for x in dbjson.keys()])

    msg = "Conta <b>{}</b> removida!".format(key)
    delete_bill(dbjson, yearmonth, key)
    bot.send_message(message.chat.id, msg, parse_mode='HTML')


print('Wikibills em atividade...')
bot.polling()
