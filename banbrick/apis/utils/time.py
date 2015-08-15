import datetime as _datetime

from django.utils import timezone

TZINFO = timezone.get_default_timezone()


def datetime_now():
    return _datetime.datetime.now(TZINFO)


def datetime(*args, **kwargs):
    return _datetime.datetime(tzinfo=TZINFO, *args, **kwargs)


def date(*args, **kwargs):
    return _datetime.date(tzinfo=TZINFO, *args, **kwargs)
