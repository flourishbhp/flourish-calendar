from django.apps import apps as django_apps
from calendar import HTMLCalendar
from edc_appointment.models import Appointment
# from flourish_child.models import Appointment as ChildrenAppointments
from .appointment_html_builder import AppointmentHtmlBuilder

class CustomCalendar(HTMLCalendar):
    def __init__(self, year=None, month=None, session=None):
        self.year = year
        self.month = month
        self.filter = session
        super(CustomCalendar, self).__init__()

    @property
    def children_appointment_cls(self):
        return django_apps.get_model('flourish_child.appointment')

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

            d += AppointmentHtmlBuilder(event).view_build()
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
                appt_datetime__year=self.year, appt_datetime__month=self.month)
            events = list(caregiver_appointments)

        elif self.filter == 'children':
            child_appointments = self.children_appointment_cls.objects.filter(
                appt_datetime__year=self.year, appt_datetime__month=self.month)
            events = list(child_appointments)

        else:
            caregiver_appointments = Appointment.objects.filter(
                appt_datetime__year=self.year, appt_datetime__month=self.month)

            child_appointments = self.children_appointment_cls.objects.filter(
                appt_datetime__year=self.year, appt_datetime__month=self.month)

            events.extend(list(caregiver_appointments))
            events.extend(list(child_appointments))

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal
