import xadmin
from xadmin import views

from core import models

from .item import (
    MonitorItemAdmin,
)
from .project import (
    ProjectAdmin,
)


class BaseAdminViewSetting(object):
    enable_themes = True
    use_bootswatch = True

xadmin.site.register(views.BaseAdminView, BaseAdminViewSetting)


class CommAdminViewSetting(object):
    global_models_icon = {
        models.ProjectTag: 'fa fa-tag', models.MonitorItemTag: 'fa fa-tag',
        models.Project: 'fa fa-laptop', models.MonitorItem: 'fa fa-magic',
    }

xadmin.site.register(views.CommAdminView, CommAdminViewSetting)


class SimpleTagAdmin(object):
    list_display = (
        'id', 'name', 'created_on', 'updated_on',
    )
    search_fields = (
        'name',
    )
    list_filter = (
        'created_on', 'updated_on',
    )
    list_display_links = (
        'id', 'name',
    )

xadmin.site.register(models.ProjectTag, SimpleTagAdmin)
xadmin.site.register(models.MonitorItemTag, SimpleTagAdmin)
