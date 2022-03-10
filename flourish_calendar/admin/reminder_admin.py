from django.contrib import admin
from ..models import Reminder
from ..forms import ReminderForm
from ..admin_site import flourish_calendar_admin
from edc_model_admin import audit_fieldset_tuple


@admin.register(Reminder, site=flourish_calendar_admin)
class ReminderAdmin(admin.ModelAdmin):

    form = ReminderForm

    fieldsets = (
        (None, {
            'fields': (
                'datetime',
                'title',
                'description',
                'status',)}
         ), audit_fieldset_tuple)

    radio_fields = {
        'status': admin.VERTICAL
    }

