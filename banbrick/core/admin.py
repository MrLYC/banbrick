from django.contrib import admin

from . import models


class SimpleModelAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.MonitorItem, SimpleModelAdmin)


class SimpleTagAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.ProjectTag, SimpleTagAdmin)
admin.site.register(models.MonitorItemTag, SimpleTagAdmin)


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    pass
