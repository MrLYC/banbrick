from core import models

import xadmin


class SimpleModelAdmin(object):
    pass

xadmin.site.register(models.ProjectTag, SimpleModelAdmin)
xadmin.site.register(models.Project, SimpleModelAdmin)
xadmin.site.register(models.MonitorItemTag, SimpleModelAdmin)
xadmin.site.register(models.MonitorItem, SimpleModelAdmin)
