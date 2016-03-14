import datetime
import calendar

'''
    String Functions
'''


def capitalize_str(descr):
    descr_cap = [d.capitalize() for d in descr.split()]
    return ' '.join(descr_cap)


'''
    Date Functions
'''


def add_months(p_date, months):
    month = p_date.month - 1 + months
    year = int(p_date.year + month / 12)
    month = month % 12 + 1
    day = min(p_date.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month=month, day=day)


def get_next_month(yearmonth):
    dt_yearmonth = datetime.datetime.strptime(yearmonth, '%Y%m')
    return add_months(dt_yearmonth, 1).strftime('%Y%m')


'''
    Message Templates
'''

msg_new_templ = msg = """
Informe a nova conta no formato: <b>key*|descr*|value*|status|pay_day</b>

<b>key*</b> - Chave da conta
<b>descr*</b> - Descrição da conta
<b>value*</b> - Valor da conta
<b>status</b> - Status da conta
<b>pay_day</b> - Data de Vencimento

<i>Formato:</i>

<b>key*</b> - Letras minúsculas, Traços (-) (opcional)
<b>descr*</b> - Livre, Alfanumérico somente
<b>value*</b> - Decimal <b>(Ex: 9999999.99)</b>
<b>status</b> - <b>P</b> para Pago ou <b>campo vazio</b> para Devendo
<b>pay_day</b> - <b>DD/MM/AAAA</b>

<i>(*) Campos obrigatórios</i>
"""

msg_modify_templ = """Altere a conta desejada no formato: <b>key*|attr*|new_value*</b>

<b>key*</b> - Chave da conta
<b>attr*</b> - Atributo da conta
<b>new_value*</b> - Novo valor para o atrib. da conta

<i>Formato:</i>

<b>key*</b> - Letras minúsculas, Traços (-) (opcional)
<b>attr*</b> - Letras minúsculas somente
<b>new_value*</b> - Livre**

<i>(*) Campos obrigatórios (somente </i><b>Data de Venc.</b><i> pode estar vazia)</i>
<i>(**) Informar o valor no formato do atributo a ser alterado</i>
"""

msg_detail_templ = """Informações da chave <b>{0}</b>

Descr....: <b>{1}</b>
Valor....: <b>{2:6.2f}</b>
Dt. Venc.: <b>{3}</b>
Status...: <b>{4}</b>
"""