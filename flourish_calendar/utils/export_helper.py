import datetime
import re

from django.apps import apps as django_app
from django.db.models import Q
from edc_appointment.models import Appointment
from edc_base.utils import get_utcnow

from flourish_calendar.models import ParticipantNote, Reminder

children_appointment_cls = django_app.get_model('flourish_child', 'Appointment')


def collect_events(request):
    q_objects = Q()
    search_term = request.GET.get('search_term', '')
    year = int(request.GET.get('year', get_utcnow().year))
    month = int(request.GET.get('month', get_utcnow().month))

    current_time = get_utcnow()

    if search_term:
        q_objects = Q(subject_identifier__icontains=search_term.strip())

    caregiver_appointments = Appointment.objects.filter(
        ~Q(user_modified='flourish') & q_objects,
        appt_datetime__gt=current_time)

    child_appointments = children_appointment_cls.objects.filter(
        ~Q(user_modified='flourish') & q_objects,
        appt_datetime__gt=current_time).exclude(
        schedule_name__icontains='quart'
    )

    reminders = Reminder.objects.filter(
        datetime__gt=current_time,
        title__icontains=search_term or ''
    )

    participant_notes = ParticipantNote.objects.filter(
        q_objects | Q(title__icontains=search_term or ''),
        date__gt=datetime.date.today()
    )

    fu_appts = children_appointment_cls.objects.filter(
        Q(schedule_name__icontains='_fu') & ~Q(schedule_name__icontains='qt'),
        user_modified='flourish',
        appt_datetime__gte=get_utcnow(), )

    return (list(caregiver_appointments) + list(child_appointments) + list(reminders) +
            list(participant_notes) + list(fu_appts))


def extract_cohort_name(s):
    cohort_names = [
        "c", "b", "a", "b_fu", "a_fu", "b_fu", "c_fu",
        "c_sec", "a_sec", "b_sec", "child_b", "child_c",
        "child_c_sq", "child_a_sq", "child_b_sq", "child_a"
    ]

    sorted_cohort_names = sorted(cohort_names, key=len, reverse=True)

    pattern = '|'.join(sorted_cohort_names)

    match = re.search(pattern, s)

    if match:
        return match.group()

    return ''
