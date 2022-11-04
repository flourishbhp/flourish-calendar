from django import forms
from django.apps import apps as django_apps
from django.forms import ValidationError

from ..models import ParticipantNote


class ParticipantNoteForm(forms.ModelForm):

    subject_consent_model = 'flourish_caregiver.subjectconsent'

    child_consent_model = 'flourish_caregiver.caregiverchildconsent'

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title = self.initial.get('title', None)

        if self.title and ('follow up' in self.title.lower() or 'comment' in self.title.lower()):
            self.fields['title'].widget.attrs['readonly'] = True

    @property
    def subject_consent_model_cls(self):
        return django_apps.get_model(self.subject_consent_model)

    @property
    def child_consent_model_cls(self):
        return django_apps.get_model(self.child_consent_model)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].initial = 'Follow Up Schedule'

    def clean(self):
        """
        Used to check if the pid exist in the database

        Raises:
            ValidationError: Subject identifier does not exist"

        Returns:
            subject_identifier if its valid
        """

        cleaned_data = super().clean()

        subject_identifier = cleaned_data.get('subject_identifier')

        child_consent = self.child_consent_model_cls.objects.filter(
            subject_identifier=subject_identifier)

        if not child_consent:

            raise ValidationError({'subject_identifier': 'Subject identifier for child does '
                                   'not exist'})

        return cleaned_data

    title = forms.CharField(
        label='Title',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        empty_value='Follow Up Schedudle')

    class Meta:
        model = ParticipantNote
        fields = '__all__'
