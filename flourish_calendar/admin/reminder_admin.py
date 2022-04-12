from django.contrib import admin
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
                'type',
                'note',
            )}
         ), audit_fieldset_tuple)

    radio_fields = {
        'type': admin.VERTICAL
    }
