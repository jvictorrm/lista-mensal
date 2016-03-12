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


def str_to_date(str_, format_='%d/%m/%Y'):
    return datetime.datetime.strptime(str_, format_)
