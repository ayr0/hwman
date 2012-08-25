from datetime import datetime
from datetime import date
from datetime import time
from dateutil.relativedelta import relativedelta as rd

def get_datetime(s):
    '''
    Try to match the string to a datetime.
    '''
    if s.lower() == 'now':
        return datetime.now()
    if s.lower() == 'today':
        return datetime.combine(date.today(), time())
    dateformats = ('%Y-%m-%d',
        '%y-%m-%d',
        '%Y %m %d',
        '%y %m %d',
        '%d %b %Y',
        '%d %b %y',)
    datenoyearformats = ('%b %d',
        '%d %b',
        '%m %d',
        '%d %m',)
    timeformats = ('%H:%M',
        '%I:%M%p',)
    datetimeformats = ('%s %s',)
    for form in dateformats:
        try:
            return datetime.strptime(s, form)
        except ValueError:
            pass
    for form in timeformats:
        try:
            t = datetime.strptime(s, form)
            return datetime.combine(date.today(), t.time())
        except ValueError:
            pass
    for form in datenoyearformats:
        try:
            t = datetime.strptime(s, form)
            t = t.replace(year=date.today().year)
            return t
        except ValueError:
            pass
    for form_dt in datetimeformats:
        for form_d in dateformats:
            for form_t in timeformats:
                form = form_dt % (form_d, form_t)
                try:
                    return datetime.strptime(s, form)
                except ValueError:
                    pass
                form = form_dt % (form_t, form_d)
                try:
                    return datetime.strptime(s, form)
                except ValueError:
                    pass
    raise ValueError('Not a recognized datetime.')
