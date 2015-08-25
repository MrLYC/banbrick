import django

if getattr(django.conf.settings, "GEVENTPATCH", False):
    from gevent import monkey
    monkey.patch_all()

from ycyc.shortcuts import logger_quick_config

django.setup()
logger_quick_config()
