from core import models

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

xadmin.site.register(models.ProjectTag, SimpleModelAdmin)
xadmin.site.register(models.Project, SimpleModelAdmin)
xadmin.site.register(models.MonitorItemTag, SimpleModelAdmin)
xadmin.site.register(models.MonitorItem, SimpleModelAdmin)
