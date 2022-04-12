from django import forms
from ..models import Reminder

class ReminderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # if self.initial.get('title', None):
        #     self.fields['title'].disabled = True

    class Meta:
        model = Reminder
        fields = '__all__'
