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
