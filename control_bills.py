from useful import *
import json


'''
    Save/Load Database
'''


def save_database(database):
    with open('db.json', 'w') as out_json:
        json.dump(database, out_json, indent=4)


def load_database():
    return json.loads(open('db.json').read())


'''
    CRUD/Actions Bills
'''


def show_help_cmds():
    dict_cmds = {
        '/list': 'Exibir todas as contas',
        '/keys': 'Exibir todas as chaves das contas',
        '/new': 'Inserir nova conta',
        '/alt': 'Alterar algum dado da conta',
        '/detail': 'Detalhar dados da conta',
        '/del': 'Remover conta',
        '/pay': 'Pagar uma conta',
        '/owe': 'Dever uma conta',
        '/wiki': 'Exibir todas os comandos para usar o Wikibills',
        '/turn_month': 'Faz a virada do mês'
    }

    msg = ''
    for k, v in dict_cmds.items():
        msg += '<b>{0}</b><pre> - {1}</pre>\n'.format(k, v)
    return msg


def show_bills(database, yearmonth):
    output_bills = ''
    sum_expense = 0
    sum_receipt = 0

    # Show 'yearmonth' as a title
    output_bills += '<b>' + yearmonth + '</b>\n'
    output_bills += '<pre>' + ('-' * 25) + '</pre>\n'

    # Get receipt
    for k, v in database[yearmonth]['receipt'].items():
        sum_receipt += v['value']

    # Get expense
    for k, v in database[yearmonth]['expense'].items():
        sum_expense += v['value']

        output_bills += '<pre>{0:<15s} {1:6.2f} {2}</pre>'\
                        .format(v['descr'][:13],
                                v['value'],
                                ('P' if v['status'] else 'D')) + '\n'

    output_bills += '<pre>' + ('-' * 25) + '</pre>\n'
    output_bills += '<pre>{0:<15s} {1:6.2f}</pre>'.format('Receita', sum_receipt) + '\n'
    output_bills += '<pre>{0:<15s} {1:6.2f}</pre>'.format('Despesa', sum_expense) + '\n'
    output_bills += '<pre>' + ('-' * 25) + '</pre>\n'
    output_bills += '<pre>{0:<15s} {1:6.2f}</pre>'.format('Saldo', sum_receipt - sum_expense)
    return output_bills


def show_bills_keys(database, yearmonth):
    out_bills_keys = ''

    # Get expense
    for k, v in database[yearmonth]['expense'].items():
        out_bills_keys += '<b>{0}</b>'.format(k)
        out_bills_keys += '<pre>{0:>15s}</pre>\n'.format(v['descr'][:13])
    return out_bills_keys


def new_bill(database, yearmonth, key, descr, value, status=False, pay_day=''):
    database[yearmonth]['expense'][key.lower()] = {
            'descr': capitalize_str(descr),
            'value': value,
            'pay_day': pay_day,
            'status': status
    }

    save_database(database)


def delete_bill(database, yearmonth, key):
    del database[yearmonth]['expense'][key]
    save_database(database)


def alter_bill(database, yearmonth, key, attr, new_value):
    if attr in ['descr']:
        database[yearmonth]['expense'][key][attr] = capitalize_str(new_value)
    else:
        database[yearmonth]['expense'][key][attr] = new_value

    save_database(database)


def change_status_bill(database, yearmonth, key, status):
    database[yearmonth]['expense'][key]['status'] = status
    save_database(database)

'''
    Month Actions
'''


def change_month_activity(database, yearmonth):
    dict_next_month = database[yearmonth]

    for k, v in dict_next_month['expense'].items():
        v['status'] = False

    database[get_next_month(yearmonth)] = dict_next_month
    del database[yearmonth]
    save_database(database)
