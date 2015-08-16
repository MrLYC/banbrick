from core import models

import xadmin


class MonitorItemAdmin(object):
    list_display = (
        'id', 'name', 'status', 'created_on', 'updated_on',
        'value', 'type', 'project', 'tag_set',
    )
    search_fields = (
        'name',
    )
    list_filter = (
        'status', 'created_on', 'updated_on',
        'type', 'project', 'tag_set',
    )
    list_display_links = (
        'id', 'name',
    )
    refresh_times = (3, 10, 60, 120, 180, 300, 600)

xadmin.site.register(models.MonitorItem, MonitorItemAdmin)


class MonitorItemHistoryAdmin(object):
    list_display = (
        'id', 'item', 'user', 'status', 'value',
    )
    search_fields = (
        'user', 'item', 'status',
    )
    list_filter = (
        'user', 'item', 'status', 'created_on', 'updated_on',
    )
    list_display_links = (
        'id',
    )
    refresh_times = (3, 10, 60, 120, 180, 300, 600)

xadmin.site.register(models.MonitorItemHistory, MonitorItemHistoryAdmin)
