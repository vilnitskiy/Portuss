import datetime
from dateutil.relativedelta import relativedelta
from django import template
register = template.Library()


@register.simple_tag
def commentator_age(self):
    age = relativedelta(
        datetime.datetime.now().date(),
        self).years
    s = ''
    if age > 1:
        s = 's'
    return str(age) + ' year%s old' % (s)
