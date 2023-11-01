from edc_form_validators import FormValidator
from django import forms


class NoteFormValidator(FormValidator):
    def clean(self):
        self.validate_against_enddate(cleaned_data=self.cleaned_data)
        super().clean()

    def validate_against_enddate(self, cleaned_data=None):
        startdate = cleaned_data.get('start_date')
        enddate = cleaned_data.get('end_date')
        if startdate and enddate:
            if enddate < startdate:
                raise forms.ValidationError(
                    "End date  cannot be before start date.")
