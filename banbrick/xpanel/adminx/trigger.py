from django.utils.translation import ugettext_lazy as _

from core import models

import xadmin


class TriggerAdmin(object):
    list_display = (
        'id', 'name', 'status', 'active', 'active_on', '__str__',
        'created_on', 'updated_on',
    )
    search_fields = (
        'user', 'status',
    )
    list_filter = (
        'name', 'status', 'active', 'active_on', 'item',
        'created_on', 'updated_on',
    )
    list_display_links = (
        'id', 'name',
    )
    fields = (
        'name', 'description', 'status',
        'item', 'operator', 'value',
        'alert_user_set', 'active', 'active_on',
    )
    refresh_times = (3, 10, 60, 120, 180, 300, 600)

xadmin.site.register(models.Trigger, TriggerAdmin)
