
from calendar import HTMLCalendar
from datetime import datetime
import imp
from sys import api_version
from django.apps import apps as django_apps
from edc_appointment.models import Appointment
from flourish_child.models import Appointment as ChildrenAppointments
from edc_appointment.choices import (
    NEW_APPT,
    IN_PROGRESS_APPT,
    INCOMPLETE_APPT,
    COMPLETE_APPT,
    CANCELLED_APPT)

class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None, session=None):
        self.year = year
        self.month = month
        self.filter = session
        super(Calendar, self).__init__()

    # formats a day as a td
    # filter events by day
    def formatday(self, day, events):

        events_per_day = []
        for event in events:
            if event.appt_datetime.day == day:
                events_per_day.append(event)

        # events_per_day = events.filter(appt_datetime__day=day)
        d = ''

        for event in events_per_day:


            appointment_display_helper = AppointmentDisplayHelper(event)
            # color = appointment_wrapper.status_color

            if not appointment_display_helper.is_child:
                d += f'''\
                    <div>
                        <li><a target="__blank" href="/subject/subject_dashboard/{appointment_display_helper.subject_identifier}/">{appointment_display_helper.html_wrapped_subject_identifier} </li>
                    </div>
				'''
            else: 
                d += f'''\
                    <div>
                        <li><a target="__blank" href="/subject/child_dashboard/{appointment_display_helper.subject_identifier}/">{appointment_display_helper.html_wrapped_subject_identifier}</li>
                    </div>
				'''

	    # <a target="__blank" href="/subject/subject_dashboard/{appointment_wrapper.model_obj.subject_identifier}/">{appointment_wrapper.model_obj.subject_identifier} <span>{appointment_wrapper.status_color}</span></a>


        if day != 0:
            return f'''\
                <td>
                    <span class='date'>{day}</span>
                    <ul> {d} </ul>
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
        
        if self.filter == 'caregiver':
            caregiver_appointments = Appointment.objects.filter(
                appt_datetime__year=self.year, appt_datetime__month=self.month)
            events = list(caregiver_appointments)

        elif self.filter == 'children':
            child_appointments = ChildrenAppointments.objects.filter(
                appt_datetime__year=self.year, appt_datetime__month=self.month)
            events = list(child_appointments)

        else:
            caregiver_appointments = Appointment.objects.filter(
                appt_datetime__year=self.year, appt_datetime__month=self.month)

            child_appointments = ChildrenAppointments.objects.filter(
                appt_datetime__year=self.year, appt_datetime__month=self.month)

            events.extend(list(caregiver_appointments))
            events.extend(list(child_appointments))
            # children_appointments = ChildrenAppointments.objects.filter(
            #     appt_datetime__year=self.year, appt_datetime__month=self.month)

            # events = cargiver_appointments | children_appointments

        print(self.filter)

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal

# TODO: Change it to a wrapper
class AppointmentDisplayHelper:

    child_appointment_model = 'flourish_child.appointment'

    def __init__(self, appointment) -> None:
        self._appointment = appointment
        self._subject_identifier = self._appointment.subject_identifier

    @property
    def model_obj(self):
        return self._appointment

    @property
    def is_child(self):
        return isinstance(self._appointment, ChildrenAppointments)
    @property
    def html_wrapped_subject_identifier(self):
        """
        NEW_APPT,
        IN_PROGRESS_APPT,
        INCOMPLETE_APPT,
        COMPLETE_APPT,
        CANCELLED_APPT⚠️⚠️
        """
        status = self._appointment.appt_status
        if status == NEW_APPT:
            return f'''\
                <span style="color: orange;" title="New Appointment">{self.subject_identifier} </span>
                '''
        elif status == IN_PROGRESS_APPT:
            return f'''\
                <span style="color: blue;" class="blink-one" title="Inprogress Appointment">{self.subject_identifier}</span>
                '''
        elif status == COMPLETE_APPT:
            return f'''\
                <span style="color: green;" title="Complete Appointment">{self.subject_identifier} ✅</span>
                '''
        elif status == INCOMPLETE_APPT:
            return f'''\
                <span style="color: green;" title="Incomplete Appointment">{self.subject_identifier} ⚠️</span>
                '''
        elif (status == CANCELLED_APPT):
            return f'''\
                <span style="color: red;" title="Cancelled Appointment">{self.subject_identifier }</span>
                '''
    @property
    def status(self):
        return self._appointment.appt_status.replace("_", " ").title()

    @property
    def subject_identifier(self):
        return self._subject_identifier
