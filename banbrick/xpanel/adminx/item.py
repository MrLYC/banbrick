from core import models

import xadmin


class MonitorItemAdmin(object):
    list_display = (
        'id', 'name', 'status', 'created_on', 'updated_on', 'key',
        'value', 'type', 'project', 'tag_set',
    )
    search_fields = (
        'name', 'key',
    )
    list_filter = (
        'status', 'created_on', 'updated_on',
        'type', 'project', 'tag_set',
    )

xadmin.site.register(models.MonitorItem, MonitorItemAdmin)
