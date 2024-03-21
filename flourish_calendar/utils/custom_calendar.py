from calendar import HTMLCalendar
from datetime import datetime, date

from django.apps import apps as django_apps
from django.db.models import Q
from requests import request

from edc_appointment.constants import NEW_APPT
from edc_appointment.models import Appointment
from edc_base.utils import get_utcnow

from ..models import ParticipantNote, Reminder
from .appointment_html_builder import AppointmentHtmlBuilder
from .reminder_html_builder import ReminderHtmlBuilder
from edc_facility.models import Holiday


class CustomCalendar(HTMLCalendar):

    def __init__(self, year=None, month=None, request=None):
        self.year = year
        self.month = month
        self.filter = request.session.get('filter', None)
        self.search_term = request.session.get('search_term', None)
        self.request = request
        super(CustomCalendar, self).__init__()

    @property
    def children_appointment_cls(self):
        return django_apps.get_model('flourish_child.appointment')

    # formats a day as a td
    # filter events by day
    def formatday(self, day, events, month):

        events_per_day = []
        for event in events:
            if isinstance(event, self.children_appointment_cls) or isinstance(event, Appointment):
                if event.appt_datetime.day == day:
                    events_per_day.append(event)
            elif isinstance(event, Reminder):
                if event.datetime.day == day:
                    events_per_day.append(event)

            elif isinstance(event, ParticipantNote):
                if event.date.day == day:
                    events_per_day.append(event)

        d = ''
        appointment_counter = 0
        reminder_counter = 0
        participant_note_counter = 0

        for event in events_per_day:
            if isinstance(event, self.children_appointment_cls) or isinstance(event, Appointment):
                d += AppointmentHtmlBuilder(event, self.request).view_build()
                appointment_counter += 1
            elif isinstance(event, Reminder):
                d += ReminderHtmlBuilder(event).view_build()
                reminder_counter += 1

            elif isinstance(event, ParticipantNote):
                d += ReminderHtmlBuilder(event).view_build()
                participant_note_counter += 1

        if day and month:

            today_day = datetime.today().day
            if self.is_holiday(date(self.year, month, day)):
                return f'''\
                    <td>
                        <span class='date {"today" if day == today_day else ""}'>{day}</span>
                        <span class='holiday-banner'>Public Holiday</span>
                        <ul style="height: 200px; overflow: scroll;"> {d} </ul>
                        <p align="center" style="padding-top: 2px; margin-botton: 1 px; border-top: 1px solid #17a2b8;" >A ({appointment_counter}) R ({reminder_counter}) N ({participant_note_counter})</p>
                    </td>
                    '''
            return f'''\
                    <td>
                        <span class='date {"today" if day == today_day else ""}'>{day}</span>
                        <ul style="height: 200px; overflow: scroll;"> {d} </ul>
                        <p align="center" style="padding-top: 2px; margin-botton: 1 px; border-top: 1px solid #17a2b8;" >A ({appointment_counter}) R ({reminder_counter}) N ({participant_note_counter})</p>
                    </td>
                    '''
        return '<td></td>'

    # formats a week as a tr
    def formatweek(self, theweek, events, month):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events, month)
        return f'<tr> {week} </tr>'

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, withyear=True):

        events = list()

        q_objects = Q()

        if self.search_term:
            q_objects = Q(subject_identifier__icontains=self.search_term)

        if self.filter == 'reminder':
            reminders = Reminder.objects.filter(
                Q(datetime__year=self.year) &
                Q(datetime__month=self.month)
            )
            events = list(reminders)

        elif self.filter == 'caregiver':
            caregiver_appointments = Appointment.objects.filter(
                ~Q(user_modified='flourish') & q_objects,
                appt_datetime__year=self.year,
                appt_datetime__month=self.month)
            events = list(caregiver_appointments)

        elif self.filter == 'children':
            child_appointments = self.children_appointment_cls.objects.filter(
                ~Q(user_modified='flourish') & q_objects,
                appt_datetime__year=self.year,
                appt_datetime__month=self.month).exclude(
                schedule_name__icontains='quart'
            )
            events = list(child_appointments)

        elif self.filter == 'reminder':
            reminders = Reminder.objects.filter(
                datetime__year=self.year, datetime__month=self.month
            )
            events = list(reminders)

        elif self.filter == 'participant_notes':
            participant_notes = ParticipantNote.objects.filter(
                date__year=self.year, date__month=self.month
            )
            events = list(participant_notes)

        elif self.filter == 'facet':
            participant_notes = ParticipantNote.objects.filter(
                date__year=self.year, date__month=self.month,
                title__icontains='facet'
            )

            reminders = Reminder.objects.filter(
                datetime__year=self.year, datetime__month=self.month,
                title__icontains='facet'
            )
            events = list(participant_notes)
            events.extend(reminders)

        elif self.filter == 'follow_up':
            participant_notes = ParticipantNote.objects.filter(
                q_objects,
                title__icontains='Follow Up Schedule',
                date__year=self.year, date__month=self.month
            )

            events = list(participant_notes)

        elif self.filter in ['a', 'b', 'c']:
            secondary_schedule_names = Appointment.objects.filter(schedule_name__icontains='_sec') \
                .values_list('schedule_name', flat=True) \
                .distinct()

            caregiver_appointments = Appointment.objects.filter(
                q_objects,
                appt_datetime__year=self.year,
                appt_datetime__month=self.month,
                schedule_name__istartswith=self.filter).exclude(
                schedule_name__in=secondary_schedule_names
            )
            events = list(caregiver_appointments)

        elif self.filter in ['a_sec', 'b_sec', 'c_sec']:
            caregiver_appointments = Appointment.objects.filter(
                q_objects,
                appt_datetime__year=self.year,
                appt_datetime__month=self.month,
                schedule_name__istartswith=self.filter)

            events = list(caregiver_appointments)
        else:
            caregiver_appointments = Appointment.objects.filter(
                ~Q(user_modified='flourish') & q_objects,
                appt_datetime__year=self.year,
                appt_datetime__month=self.month)

            child_appointments = self.children_appointment_cls.objects.filter(
                ~Q(user_modified='flourish') & q_objects,
                appt_datetime__year=self.year,
                appt_datetime__month=self.month, ).exclude(
                schedule_name__icontains='quart'
            )

            reminders = Reminder.objects.filter(
                datetime__year=self.year, datetime__month=self.month,
                title__icontains=self.search_term or ''
            )

            participant_notes = ParticipantNote.objects.filter(
                q_objects | Q(title__icontains=self.search_term or ''),
                date__year=self.year, date__month=self.month
            )

            events.extend(list(reminders))
            events.extend(list(participant_notes))
            events.extend(list(caregiver_appointments))
            events.extend(list(child_appointments))

        events = list(filter(lambda e: 'comment' not in getattr(e, 'title', '').lower(),
                             events))

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events, self.month)}\n'
        return cal

    def is_holiday(self, date_to_check):

        holiday = Holiday.objects.filter(local_date=date_to_check).exists()

        return holiday
