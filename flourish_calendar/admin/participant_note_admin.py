from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple
from edc_model_admin.model_admin_basic_mixin import ModelAdminBasicMixin
from edc_model_admin.model_admin_next_url_redirect_mixin import ModelAdminNextUrlRedirectMixin

from ..admin_site import flourish_calendar_admin
from ..forms import ParticipantNoteForm
from ..models import ParticipantNote


@admin.register(ParticipantNote, site=flourish_calendar_admin)
class ParticipantNoteAdmin(ModelAdminBasicMixin,
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

    search_fields = ('subject_identifier', 'title', )

    list_display = ('subject_identifier', 'title', 'date', 'color', )

    list_filter = ('title', 'date', 'color', )
