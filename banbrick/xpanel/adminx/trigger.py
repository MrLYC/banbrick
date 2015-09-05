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

    def setup_forms(self):
        user = self.request.user
        super(TriggerAdmin, self).setup_forms()
        fields = self.form_obj.fields
        if user.is_superuser:
            return

        item_field = fields["item"]
        item_field.queryset = item_field.queryset.filter(
            project__group__in=user.groups.all()
        )
        trigger_ins = self.form_obj.instance
        alert_user_set_field = fields["alert_user_set"]
        alert_user_set_field.queryset = (
            trigger_ins.alert_user_set.all() |
            alert_user_set_field.queryset.filter(
                groups__in=user.groups.all()
            )
        )

    def get_list_queryset(self):
        qs = super(TriggerAdmin, self).get_list_queryset()
        user = self.request.user
        if user.is_superuser:
            return qs
        return qs.filter(item__project__group__in=user.groups.all())

xadmin.site.register(models.Trigger, TriggerAdmin)
