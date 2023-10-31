from django import forms
from ..models import Reminder
from edc_form_validators import FormValidatorMixin
from ..form_validations import NoteFormValidator


class ReminderForm(FormValidatorMixin, forms.ModelForm):
    form_validator_cls = NoteFormValidator

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # if self.initial.get('title', None):
        #     self.fields['title'].disabled = True

    class Meta:
        model = Reminder
        fields = '__all__'
