
from calendar import HTMLCalendar
from datetime import datetime
import imp
from select import select
from sys import api_version
from xml.etree.ElementPath import prepare_parent
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
        appointments = 0

        for event in events_per_day:


            d += AppointmentDisplayHelper(event).view_build()
            appointments += 1


        if day != 0:
            return f'''\
                <td>
                    <span class='date'>{day}</span>
                    <ul style="height: 200px; overflow: scroll;"> {d} </ul>
                    <p align="center" style="padding-top: 2px; margin-botton: 1 px; border-top: 1px solid #17a2b8;" >{appointments} Appointment(s)</p>
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
                timepoint_datetime__year=self.year, timepoint_datetime__month=self.month)
            events = list(caregiver_appointments)

        elif self.filter == 'children':
            child_appointments = ChildrenAppointments.objects.filter(
                timepoint_datetime__year=self.year, timepoint_datetime__month=self.month)
            events = list(child_appointments)

        else:
            caregiver_appointments = Appointment.objects.filter(
                timepoint_datetime__year=self.year, timepoint_datetime__month=self.month)

            child_appointments = ChildrenAppointments.objects.filter(
                timepoint_datetime__year=self.year, timepoint_datetime__month=self.month)

            events.extend(list(caregiver_appointments))
            events.extend(list(child_appointments))
            # children_appointments = ChildrenAppointments.objects.filter(
            #     timepoint_datetime__year=self.year, timepoint_datetime__month=self.month)

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

    def __init__(self, appointment: Appointment) -> None:
        self._appointment = appointment
        self._subject_identifier = self._appointment.subject_identifier

    @property
    def model_obj(self):
        return self._appointment

    @property
    def is_child(self):
        return isinstance(self._appointment, ChildrenAppointments)
    @property
    def html_wrapped_status(self):
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
                <span style="color: orange;" title="New Appointment">{self.status} </span>
                '''
        elif status == IN_PROGRESS_APPT:
            return f'''\
                <span style="color: blue;" class="blink-one" title="Inprogress Appointment">{self.status}</span>
                '''
        elif status == COMPLETE_APPT:
            return f'''\
                <span style="color: green;" title="Complete Appointment">{self.status} ✅</span>
                '''
        elif status == INCOMPLETE_APPT:
            return f'''\
                <span style="color: green;" title="Incomplete Appointment">{self.status} ⚠️</span>
                '''
        elif (status == CANCELLED_APPT):
            return f'''\
                <span style="color: red;" title="Cancelled Appointment">{self.status }</span>
                '''
    @property
    def status(self):
        return self._appointment.appt_status.replace("_", " ").title()

    @property
    def subject_identifier(self):
        return self._subject_identifier
    
    @property
    def visit_code(self):
        return self._appointment.visit_code

    @property
    def previous_appointments(self):
        return self._appointment.history.all()

    @property
    def resceduled_appointments_count(self):

        prev_appt = self.previous_appointments.values_list(
            'timepoint_datetime__date', flat=True)
        prev_appt_set = set(prev_appt)
        return len(prev_appt_set) - 1

    @property
    def last_appointment(self):

        appt = self.previous_appointments.exclude(
            timepoint_datetime__date=self._appointment.appt_datetime.date())

        if appt:
            return appt.last().appt_datetime.date()
        else:
            return None

    def _html(self, dashboard_type):
        view = "<div class='item'><li>"

        view += f"""\
            <a target="__blank" href="/subject/{dashboard_type}/{self.subject_identifier}/">
                <b>{self.subject_identifier}</b>
            </a>
                <br/>
                Visit Code : {self.visit_code}
                <br/>
                Status : {self.html_wrapped_status}
            """

        if self.resceduled_appointments_count:
            view += f"""\
                <br>
                Reschedules: {self.resceduled_appointments_count}
                """
        if self.last_appointment:
            view += f"""\
                <br>
                Prev. Appt Date: {self.last_appointment}
                """

        view += "</li></div>"

        return view


    def view_build(self):


        if self.is_child:
            return self._html('child_dashboard')
        else:
            return self._html('subject_dashboard')


        

