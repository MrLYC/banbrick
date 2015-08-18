from django.utils.translation import ugettext_lazy as _

from core import models

import xadmin


class TriggerConditionAdmin(object):
    list_display = (
        'id', '__str__', 'trigger', 'created_on', 'updated_on',
    )
    search_fields = (
        'variable',
    )
    list_filter = (
        'trigger', 'created_on', 'updated_on',
        'variable',
    )
    list_display_links = (
        'id', '__str__',
    )
    fields = ('trigger', 'variable', 'operator', 'type', 'value')

xadmin.site.register(models.Condition, TriggerConditionAdmin)


class TriggerAdmin(object):
    list_display = (
        'id', 'name', 'status', 'active', 'active_on', 'item',
        'created_on', 'updated_on',
    )
    search_fields = (
        'user', 'item', 'status',
    )
    list_filter = (
        'name', 'status', 'active', 'active_on', 'item',
        'created_on', 'updated_on',
    )
    list_display_links = (
        'id', 'name',
    )
    refresh_times = (3, 10, 60, 120, 180, 300, 600)

xadmin.site.register(models.Trigger, TriggerAdmin)
