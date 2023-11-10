from edc_form_validators import FormValidator
from django import forms
from ..constants import ONCE


class NoteFormValidator(FormValidator):
    def clean(self):
        super().clean()
        self.validate_against_enddate()
        self.validate_repeat()

    def validate_against_enddate(self):
        start_date = self.cleaned_data.get('start_date', None)
        end_date = self.cleaned_data.get('end_date', None)

        if start_date and end_date:
            if end_date < start_date:
                raise forms.ValidationError("End date  cannot be before start date.")

    def validate_repeat(self):
        self.not_required_if(ONCE,
                             field='repeat',
                             field_required='end_date')
