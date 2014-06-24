import re


def clean_phone(phone):
    return re.sub(u'\D', u'', phone)[-10:]