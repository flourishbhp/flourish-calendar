from django.apps import apps as django_apps
from edc_appointment.models import Appointment
from edc_appointment.choices import (
    NEW_APPT,
    IN_PROGRESS_APPT,
    INCOMPLETE_APPT,
    COMPLETE_APPT,
    CANCELLED_APPT
)

class AppointmentHtmlBuilder:

    child_appointment_model = 'flourish_child.appointment'

    def __init__(self, appointment: Appointment) -> None:
        self._appointment = appointment
        self._subject_identifier = self._appointment.subject_identifier

    @property
    def children_appointment_cls(self):
        return django_apps.get_model('flourish_child.appointment')

    @property
    def model_obj(self):
        return self._appointment

    @property
    def is_child(self):
        return isinstance(self._appointment, self.children_appointment_cls)

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
            'appt_datetime__date', flat=True)
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
        view = f"<div class='item {self._appointment.appt_status}'><li>"

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
