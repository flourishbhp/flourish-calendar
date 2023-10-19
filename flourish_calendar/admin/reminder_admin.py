from django.conf import settings
from django.contrib import admin
from django.shortcuts import reverse
from edc_model_admin import audit_fieldset_tuple
from edc_model_admin import ModelAdminAuditFieldsMixin, ModelAdminBasicMixin, \
    ModelAdminFormAutoNumberMixin
from edc_model_admin.model_admin_next_url_redirect_mixin import \
    ModelAdminNextUrlRedirectMixin

from ..admin_site import flourish_calendar_admin
from ..forms import ReminderForm
from ..models import Reminder


def delete_repeating_instances(instance):
    repeating_reminders = Reminder.objects.filter(
        title=instance.title,
        note=instance.note,
        color=instance.color,
        datetime__gt=instance.datetime)
    repeating_reminders.delete()


@admin.register(Reminder, site=flourish_calendar_admin)
class ReminderAdmin(ModelAdminBasicMixin,
                    ModelAdminNextUrlRedirectMixin,
                    ModelAdminFormAutoNumberMixin,
                    ModelAdminAuditFieldsMixin,
                    admin.ModelAdmin):
    form = ReminderForm

    fieldsets = (
        (None, {
            'fields': (
                'start_date',
                'end_date',
                'remainder_time',
                'title',
                'note',
                'repeat',
                'color',
            )}
         ), audit_fieldset_tuple)

    radio_fields = {
        'color': admin.VERTICAL,
        'repeat': admin.HORIZONTAL
    }

    def redirect_url_on_delete(self, request, obj_display, obj_id):
        url = settings.DASHBOARD_URL_NAMES.get('flourish_calendar_url')
        return reverse(url)

    def delete_model(self, request, obj):
        delete_repeating_instances(obj)
        super().delete_model(request, obj)

    def delete_reminder_with_repeating_instances(self, request, queryset):
        for obj in queryset:
            delete_repeating_instances(obj)

    delete_reminder_with_repeating_instances.short_description = (
        "Delete selected reminders with all following repeating instances")

    actions = [delete_reminder_with_repeating_instances]
