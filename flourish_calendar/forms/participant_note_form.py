from django import forms
from django.apps import apps as django_apps
from django.forms import ValidationError
from matplotlib.pyplot import title

from ..models import ParticipantNote


class ParticipantNoteForm(forms.ModelForm):
    
    
    child_consent_model = 'flourish_caregiver.caregiverchildconsent'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.title = self.initial.get('title', None)
        
        
        if self.title and \
                ('follow up' in self.title.lower()) or \
                ('comment' in self.title.lower()):
            self.fields['title'].widget.attrs['readonly'] = True

        
    
    @property
    def child_consent_model_cls(self):
        return django_apps.get_model(self.child_consent_model)

        
    def clean(self):
        """
        Used to check if the pid exist in the database

        Raises:
            ValidationError: Subject identifier does not exist"

        Returns:
            subject_identifier if its valid
        """
        
        cleaned_data = super().clean()
        
        title = cleaned_data.get('title', None)

        
        if title and title == 'Follow Up':
            
            subject_identifier = cleaned_data['subject_identifier'] #can never be blank
            
            if not self.child_consent_model_cls.objects.filter(subject_identifier=subject_identifier).exists():
                    
                raise ValidationError({'subject_identifier':'Subject identifier does not exist'})
                
        return cleaned_data 

    class Meta:
        model = ParticipantNote
        fields = '__all__'
