from django.contrib import admin
from django.conf import settings
from django.shortcuts import redirect, reverse
from ..models import Reminder
from ..forms import ReminderForm
from ..admin_site import flourish_calendar_admin
from edc_model_admin import audit_fieldset_tuple
from edc_model_admin.model_admin_basic_mixin import ModelAdminBasicMixin
from edc_model_admin.model_admin_next_url_redirect_mixin import ModelAdminNextUrlRedirectMixin


@admin.register(Reminder, site=flourish_calendar_admin)
class ReminderAdmin(
        ModelAdminBasicMixin,
        ModelAdminNextUrlRedirectMixin,
        admin.ModelAdmin):

    form = ReminderForm

    fieldsets = (
        (None, {
            'fields': (
                'datetime',
                'title',
                'note',
                'color',
            )}
         ), audit_fieldset_tuple)
    
    radio_fields = {
        'color': admin.VERTICAL
    }

    
    def redirect_url_on_delete(self, request, obj_display, obj_id):
        url = settings.DASHBOARD_URL_NAMES.get('flourish_calendar_url')
        return reverse(url)
