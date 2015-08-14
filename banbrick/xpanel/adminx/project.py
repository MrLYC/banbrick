from core import models
import xadmin


class ProjectAdmin(object):
    list_display = (
        'id', 'name', 'status', 'created_on', 'updated_on',
        'description', 'group', 'tag_set',
    )
    search_fields = (
        'name', 'description',
    )
    list_filter = (
        'status', 'created_on', 'updated_on',
        'group', 'tag_set',
    )

xadmin.site.register(models.Project, ProjectAdmin)
