from core import models
from django.utils.translation import ugettext_lazy as _

import xadmin
from xadmin import views


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


class SimpleModelAdmin(object):
    pass


class SimpleTagAdmin(object):
    list_display = (
        'id', 'name', 'created_on', 'updated_on',
    )

xadmin.site.register(models.ProjectTag, SimpleTagAdmin)
xadmin.site.register(models.MonitorItemTag, SimpleTagAdmin)


class ProjectAdmin(object):
    list_display = (
        'id', 'name', 'status', 'created_on', 'updated_on',
        'description', 'group', 'tag_set',
    )

xadmin.site.register(models.Project, ProjectAdmin)


class ProjectAdmin(object):
    list_display = (
        'id', 'name', 'status', 'created_on', 'updated_on', 'key',
        'value', 'type', 'project', 'tag_set',
    )

xadmin.site.register(models.MonitorItem, ProjectAdmin)
