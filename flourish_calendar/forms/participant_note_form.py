import datetime
from dateutil.relativedelta import relativedelta
from django import forms
from django.apps import apps as django_apps
from django.forms import ValidationError

from ..models import ParticipantNote


class ParticipantNoteForm(forms.ModelForm):

    subject_consent_model = 'flourish_caregiver.subjectconsent'

    child_consent_model = 'flourish_caregiver.caregiverchildconsent'

    schedule_history_model = 'edc_visit_schedule.subjectschedulehistory'

    cohort_schedules_model = 'flourish_caregiver.cohortschedules'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title = self.initial.get('title', None)
        subject_identifier = self.initial.get('subject_identifier', None)

        if self.title and ('follow up' in self.title.lower() or 'comment' in self.title.lower()):
            self.fields['title'].widget.attrs['readonly'] = True
        if self.fu_contact_exists(subject_identifier):
            self.fields['date'].widget = forms.DateInput(
                attrs={'readonly': 'readonly'})

    @property
    def subject_consent_model_cls(self):
        return django_apps.get_model(self.subject_consent_model)

    @property
    def child_consent_model_cls(self):
        return django_apps.get_model(self.child_consent_model)

    @property
    def schedule_history_cls(self):
        return django_apps.get_model(self.schedule_history_model)

    @property
    def cohort_schedules_model_cls(self):
        return django_apps.get_model(self.cohort_schedules_model)

    @property
    def enrolment_schedule_names(self):
        return self.cohort_schedules_model_cls.objects.filter(
            schedule_type='enrollment',
            onschedule_model__startswith='flourish_child').values_list(
                'schedule_name', flat=True)

    def pf_booking_check(self, subject_identifier):
        try:
            consent = self.child_consent_model_cls.objects.filter(
                subject_identifier=subject_identifier,
                study_child_identifier__isnull=False).latest('consent_datetime')
        except self.child_consent_model_cls.DoesNotExist:
            return None
        else:
            return 'P' in consent.study_child_identifier

    @property
    def fu_contact_cls(self):
        return django_apps.get_model('flourish_follow.contact')

    def fu_contact_exists(self, subject_identifier):
        """ Checks if there participant is being scheduled for FU using
            the contact form. If so, then make date readonly so there's
            a single data entry point for scheduling.
            @param subject_identifier: child's identifier
        """
        return self.fu_contact_cls.objects.filter(
            subject_identifier=subject_identifier,
            appt_date__isnull=False).exists()

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
        date = cleaned_data.get('date')

        child_consent = self.child_consent_model_cls.objects.filter(
            subject_identifier=subject_identifier)

        subject_consent = self.subject_consent_model_cls.objects.filter(
            subject_identifier=subject_identifier
        )

        if not (child_consent or subject_consent):
            raise ValidationError(
                {'subject_identifier':
                 'Subject identifier for child/caregiver does not exist'})

        is_pf_child = self.pf_booking_check(subject_identifier)

        if (self.cleaned_data.get('title', '') == 'Follow Up Schedule' and
                not is_pf_child):
            onschedules = self.schedule_history_cls.objects.filter(
                subject_identifier=subject_identifier,
                schedule_name__in=self.enrolment_schedule_names)
            if onschedules and date:
                start_dt = datetime.date(2023, 1, 1)
                enrolment_dt = onschedules.earliest(
                    'onschedule_datetime').onschedule_datetime
                followup_dt = enrolment_dt + relativedelta(years=1)
                lower_bound = (followup_dt - relativedelta(days=45)).date()
                upper_bound = (followup_dt + relativedelta(days=45)).date()
                if (enrolment_dt.date() >= start_dt and (
                        date < lower_bound or date > upper_bound)):
                    raise ValidationError(
                        {'date': 'Date is outside the window period of booking'})

        return cleaned_data

    title = forms.CharField(
        label='Title',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        empty_value='Follow Up Schedule')

    class Meta:
        model = ParticipantNote
        fields = '__all__'
