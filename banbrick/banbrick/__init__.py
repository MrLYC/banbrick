import django

if getattr(django.conf.settings, "GEVENTPATCH", False):
    from gevent import monkey
    monkey.patch_all()

django.setup()
