from calendar import HTMLCalendar
from datetime import datetime

from django.apps import apps as django_apps
from django.db.models import Q
from edc_appointment.models import Appointment
from requests import request

from .appointment_html_builder import AppointmentHtmlBuilder
from .reminder_html_builder import ReminderHtmlBuilder
from ..models import Reminder


class CustomCalendar(HTMLCalendar):
    def __init__(self, year=None, month=None, request=None):
        self.year = year
        self.month = month
        self.filter = request.session.get('filter', None)
        self.search_term = request.session.get('search_term', '')
        self.request = request
        super(CustomCalendar, self).__init__()

    @property
    def children_appointment_cls(self):
        return django_apps.get_model('flourish_child.appointment')

    # formats a day as a td
    # filter events by day
    def formatday(self, day, events):

        events_per_day = []
        for event in events:
            if isinstance(event, self.children_appointment_cls) or isinstance(event, Appointment):
                if event.appt_datetime.day == day:
                    events_per_day.append(event)
            elif isinstance(event, Reminder):
                if event.datetime.day == day:
                    events_per_day.append(event)

        d = ''
        appointment_counter = 0
        reminder_counter = 0

        for event in events_per_day:
            if isinstance(event, self.children_appointment_cls) or isinstance(event, Appointment):
                d += AppointmentHtmlBuilder(event, self.request).view_build()
                appointment_counter += 1
            elif isinstance(event, Reminder):
                d += ReminderHtmlBuilder(event).view_build()
                reminder_counter += 1

        if day != 0:
            today_day = datetime.today().day
            return f'''\
                <td>
                    <span class='date {"today" if day == today_day else ""}'>{day}</span>
                    <ul style="height: 200px; overflow: scroll;"> {d} </ul>
                    <p align="center" style="padding-top: 2px; margin-botton: 1 px; border-top: 1px solid #17a2b8;" >A ({appointment_counter}) N ({reminder_counter}) </p>
                </td>
                '''
        return '<td></td>'

    # formats a week as a tr
    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, withyear=True):

        events = list()

        q_objects = Q()

        if self.search_term:
            q_objects = Q(subject_identifier__icontains=self.search_term) | \
                        Q(visit_code__icontains=self.search_term) | \
                        Q(appt_status__icontains=self.search_term) | \
                        Q(timepoint_status__icontains=self.search_term) | \
                        Q(appt_reason__icontains=self.search_term)

        if self.filter == 'reminder':
            reminders = Reminder.objects.filter(
                Q(datetime__year=self.year) &
                Q(datetime__month=self.month)
            )
            events = list(reminders)

        elif self.filter == 'caregiver':
            caregiver_appointments = Appointment.objects.filter(
                (Q(appt_datetime__year=self.year) & Q(appt_datetime__month=self.month)) & q_objects)
            events = list(caregiver_appointments)

        elif self.filter == 'children':
            child_appointments = self.children_appointment_cls.objects.filter(
                (Q(appt_datetime__year=self.year) & Q(appt_datetime__month=self.month)) & q_objects)
            events = list(child_appointments)


        elif self.filter == 'reminder':
            reminders = Reminder.objects.filter(
                datetime__year=self.year, datetime__month=self.month
            )
            events = list(reminders)

        else:
            caregiver_appointments = Appointment.objects.filter(
                (Q(appt_datetime__year=self.year) & Q(appt_datetime__month=self.month)) & q_objects)

            child_appointments = self.children_appointment_cls.objects.filter(
                (Q(appt_datetime__year=self.year) & Q(appt_datetime__month=self.month)) & q_objects)

            reminders = Reminder.objects.filter(
                datetime__year=self.year, datetime__month=self.month
            )

            events.extend(list(reminders))
            events.extend(list(caregiver_appointments))
            events.extend(list(child_appointments))

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal
    