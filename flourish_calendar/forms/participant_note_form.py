from django import forms
from django.apps import apps as django_apps
from django.forms import ValidationError

from ..models import ParticipantNote


class ParticipantNoteForm(forms.ModelForm):
    
    
    subject_consent_model = 'flourish_caregiver.subjectconsent'
    
    child_consent_model = 'flourish_caregiver.caregiverchildconsent'
    
    @property
    def subject_consent_model_cls(self):
        return django_apps.get_model(self.subject_consent_model)
    
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

        
        subject_identifier = cleaned_data['subject_identifier'] #can never be blank
        
        
        if not (self.subject_consent_model_cls.objects.filter(subject_identifier=subject_identifier).exists() or \
            self.child_consent_model_cls.objects.filter(subject_identifier=subject_identifier).exists()):
                
            raise ValidationError({'subject_identifier':'Subject identifier does not exist'})
            
        return cleaned_data 

    class Meta:
        model = ParticipantNote
        fields = '__all__'
