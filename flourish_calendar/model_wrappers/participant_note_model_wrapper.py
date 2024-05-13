from django.apps import apps as django_apps
from django.conf import settings
from edc_model_wrapper import ModelWrapper


class ParticipantNoteModelWrapper(ModelWrapper):
    model = 'flourish_calendar.participantnote'
    querystring = ['title', ]
    next_url_name = settings.DASHBOARD_URL_NAMES.get('flourish_calendar_url')
    child_consent_model = 'flourish_caregiver.caregiverchildconsent'
    cohort_model = 'flourish_caregiver.cohort'

    @property
    def comments(self):
        commments = self.model_cls.objects.filter(title__icontains='comment')
        return commments

    @property
    def child_consent_cls(self):
        return django_apps.get_model(self.child_consent_model)

    @property
    def cohort_cls(self):
        return django_apps.get_model(self.cohort_model)

    @property
    def cohort(self):
        child_cohort = self.child_consent_cls.objects.filter(
            subject_identifier=self.object.subject_identifier).only('cohort').first()
        if child_cohort and child_cohort.cohort:
            try:
                cohort_obj = self.cohort_cls.objects.get(
                    subject_identifier=self.object.subject_identifier,
                    current_cohort=True)
            except self.cohort_cls.DoesNotExist:
                pass
            else:
                return cohort_obj.name.replace('cohort_', '')

    @property
    def title(self):
        if 'follow' in self.object.title.lower() and self.cohort:
            return f'{self.object.subject_identifier}[{self.cohort.upper()}]'
        elif 'PF to Flourish Enrol' in self.object.title:
            return f'{self.object.subject_identifier}[{self.object.title.replace(" Enrol", "")}]'
        else:
            return self.object.title
