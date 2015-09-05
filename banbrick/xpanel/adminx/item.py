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
        'type', 'project', 'tag_set', 'project',
    )
    list_display_links = (
        'id', 'name',
    )
    refresh_times = (3, 10, 60, 120, 180, 300, 600)

    def setup_forms(self):
        user = self.request.user
        super(MonitorItemAdmin, self).setup_forms()
        fields = self.form_obj.fields

        project_field = fields["project"]
        project_field.queryset = project_field.queryset.filter(
            group__in=user.groups.all()
        )

    def get_list_queryset(self):
        qs = super(MonitorItemAdmin, self).get_list_queryset()
        user = self.request.user
        if user.is_superuser:
            return qs
        return qs.filter(project__group__in=user.groups.all())

xadmin.site.register(models.MonitorItem, MonitorItemAdmin)


class MonitorItemHistoryAdmin(object):
    list_display = (
        'id', 'item', 'user', 'status', 'value',
        'created_on', 'updated_on',
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

    def get_list_queryset(self):
        qs = super(MonitorItemHistoryAdmin, self).get_list_queryset()
        user = self.request.user
        if user.is_superuser:
            return qs
        return qs.filter(item__project__group__in=user.groups.all())

xadmin.site.register(models.MonitorItemHistory, MonitorItemHistoryAdmin)
