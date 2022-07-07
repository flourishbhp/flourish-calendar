from django.contrib import admin
from ..models import ParticipantNote
from ..forms import ParticipantNoteForm
from ..admin_site import flourish_calendar_admin
from edc_model_admin import audit_fieldset_tuple
from edc_model_admin.model_admin_basic_mixin import ModelAdminBasicMixin
from edc_model_admin.model_admin_next_url_redirect_mixin import ModelAdminNextUrlRedirectMixin


@admin.register(ParticipantNote, site=flourish_calendar_admin)
class ParticipantNoteAdmin(
        ModelAdminBasicMixin,
        ModelAdminNextUrlRedirectMixin,
        admin.ModelAdmin):

    form = ParticipantNoteForm
    
    fieldsets = (
        (None, {
            'fields': (
                'date',
                'subject_identifier',
                'title',
                'description',
                'color'
            )}
         ), audit_fieldset_tuple)

    radio_fields = {
        'color': admin.VERTICAL,
    }