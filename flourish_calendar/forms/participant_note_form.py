from django import forms
from ..models import ParticipantNote

class ParticipantNoteForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # if self.initial.get('title', None):
        #     self.fields['title'].disabled = True

    class Meta:
        model = ParticipantNote
        fields = '__all__'
