import telebot
import json
# import operator

"""
Setup the bot
"""
bot = telebot.TeleBot('197158727:AAGKzk9u5Q6VzbMjUPmoGPrJhcOKuTWxkew')
bot_info = bot.get_me()  # Execute an API call
result = bot_info  # Get the result of the execution

'''
print(result.id)
print(result.username)
print(result.first_name)
print(result.last_name)
'''

month = {
    '201603': {
        'claro': {'descr': 'Claro', 'value': 42, 'pay_day': '10/03/2016', 'status': False},
        'casa': {'descr': 'Casa', 'value': 150, 'pay_day': '', 'status': False},
        'nubank': {'descr': 'Nubank', 'value': 171, 'pay_day': '15/03/2016', 'status': True},
        'superxcap': {'descr': 'SuperXCap', 'value': 22.14, 'pay_day': '05/03/2016', 'status': True},
        'faculdade': {'descr': 'Faculdade', 'value': 600, 'pay_day': '07/03/2016', 'status': True},
        'netflix': {'descr': 'Netflix', 'value': 7.5, 'pay_day': '', 'status': True},
        'cabelo': {'descr': 'Cabelo', 'value': 20, 'pay_day': '', 'status': False},
        'pagar-claudio': {'descr': 'Pagar Cláudio', 'value': 23, 'pay_day': '', 'status': True}
    }
}


def save_database(database):
    with open('db.json', 'w') as out_json:
        json.dump(database, out_json, indent=4)


def load_database():
    return json.loads(open('db.json').read())


def show_bills(database):
    output_bills = ''
    sum_bills = 0
    for k1, v1 in database.items():
        for k2, v2 in v1.items():
            # print(k, v['descr'], v['pay_day'], v['value'], v['status'])
            output_bills += '{0:<15s} {1:6.2f} {2}'\
                                .format(v2['descr'],
                                        v2['value'],
                                        ('P' if v2['status'] else 'D')) + '\n'
            sum_bills += v2['value']

    output_bills += ('-' * 25) + '\n'
    output_bills += '{0:<15s} {1:6.2f}'.format('Receita', 1380) + '\n'
    output_bills += '{0:<15s} {1:6.2f}'.format('Despesa', sum_bills) + '\n'
    output_bills += ('-' * 25) + '\n'
    output_bills += '{0:<15s} {1:6.2f}'.format('Saldo', 1380 - sum_bills)
    print(output_bills)


def new_bill(database, cmonth, key, descr, value, pay_day, status=False):
    database[cmonth][key] = {
            'descr': descr,
            'value': value,
            'pay_day': pay_day,
            'status': status
    }

#save_database(month)
teste = load_database()
show_bills(teste)
new_bill(teste, '201603', 'teste', 'testando namoral', 499, '', True)
save_database(teste)
show_bills(teste)
