import datetime

from django.apps import apps as django_app
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from edc_base.utils import age, get_utcnow

from flourish_calendar.models import ParticipantNote

children_appointment_cls = django_app.get_model('flourish_child', 'Appointment')


def collect_events(request):
    q_objects = Q()
    search_term = request.GET.get('search_term', '')
    year = int(request.GET.get('year', get_utcnow().year))
    month = int(request.GET.get('month', get_utcnow().month))

    current_time = get_utcnow()

    if search_term:
        q_objects = Q(subject_identifier__icontains=search_term.strip())

    participant_notes = ParticipantNote.objects.filter(
        q_objects | Q(title__icontains=search_term or ''),
        Q(title__icontains='Follow Up Schedule'),
        date__gt=datetime.date.today()
    )

    fu_appts = children_appointment_cls.objects.filter(
        Q(schedule_name__icontains='_fu') & ~Q(schedule_name__icontains='qt'),
        user_modified='flourish',
        appt_datetime__gte=get_utcnow(), )

    return list(fu_appts) + list(participant_notes)


def extract_cohort_name(subject_identifier):
    cohort_model_cls = django_app.get_model('flourish_caregiver', 'cohort')
    try:
        cohort = cohort_model_cls.objects.filter(
            subject_identifier=subject_identifier).latest('assign_datetime')
    except cohort_model_cls.DoesNotExist:
        return None
    else:
        return cohort.name


def cohort_objs(subject_identifier):
    cohort_model = 'flourish_caregiver.cohort'
    cohort_model_cls = django_app.get_model(cohort_model)
    return cohort_model_cls.objects.filter(
        subject_identifier=subject_identifier)


def enrolment_cohort(subject_identifier):
    try:
        return cohort_objs(subject_identifier).filter(
            enrollment_cohort=True).latest('assign_datetime')
    except ObjectDoesNotExist:
        return None


def current_cohort(subject_identifier):
    try:
        return cohort_objs(subject_identifier).filter(
            current_cohort=True).latest('assign_datetime')
    except ObjectDoesNotExist:
        return None


def get_child_age(subject_identifier=None):
    caregiver_child_consent_model = 'flourish_caregiver.caregiverchildconsent'
    caregiver_child_consent_cls = django_app.get_model(caregiver_child_consent_model)
    try:
        consent = caregiver_child_consent_cls.objects.filter(
            subject_identifier=subject_identifier).latest('consent_datetime')
    except caregiver_child_consent_cls.DoesNotExist:
        return None
    else:
        _age = age(consent.child_dob, get_utcnow())
        return _age.years + _age.months / 12
