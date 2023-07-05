from django.apps import apps as django_apps
from django.conf import settings
from edc_model_wrapper import ModelWrapper


class ParticipantNoteModelWrapper(ModelWrapper):

    model = 'flourish_calendar.participantnote'
    child_consent_model = 'flourish_caregiver.caregiverchildconsent'
    querystring = ['title', ]
    next_url_name = settings.DASHBOARD_URL_NAMES.get('flourish_calendar_url')

    @property
    def title(self):
        return self.object.title


    @property
    def comments(self):
        commments = self.model_cls.objects.filter(title__icontains='comment')
        return commments

    @property
    def child_consent_cls(self):
        return django_apps.get_model(self.child_consent_model)

    @property
    def cohort(self):
        child_cohort = self.child_consent_cls.objects.filter(
            subject_identifier=self.object.subject_identifier).only('cohort').first()
        if child_cohort:
            return getattr(child_cohort, 'cohort').replace('cohort_', '')
