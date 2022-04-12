import imp
from django.apps import apps as django_apps
from edc_appointment.models import Appointment
from ..model_wrappers import ReminderModelWrapper
from ..models import Reminder
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
                <span style="color: red;" title="Cancelled Appointment">{self.status}</span>
                '''

    @property
    def status(self):
        return self._appointment.appt_status.replace("_", " ").title()

    @property
    def status_color(self):
        status = self._appointment.appt_status

        if status == NEW_APPT:
            return 'label-warning'
        elif status == COMPLETE_APPT:
            return 'label-success'
        elif status == INCOMPLETE_APPT:
            return 'label-info'
        elif status == CANCELLED_APPT:
            return 'label-warning'
        elif status == IN_PROGRESS_APPT:
            return 'label-default'

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

    @property
    def reminder(self):
        reminder = Reminder()
        return ReminderModelWrapper(model_obj=reminder)

    @property
    def add_reschedule_reason(self):
        # if self.resceduled_appointments_count:
        return f'''<br> <a href='{self.reminder.href}title = {self.subject_identifier} - Rescedule reason'></a> '''

    def _html(self, dashboard_type):
        view = f'''\
        <div class="appointment-container" style="border:none">
            <button 
            class="label {self.status_color} appointment" 
            id="appointment"
            data-toggle="popover" 
            title="<a target='__blank' \
                href='/subject/{dashboard_type}/{self.subject_identifier}/'>Dashboard</a>" 
            data-content="Visit Code : {self.visit_code}<br> Status : {self.status} \
            <br> Reschedules: {self.resceduled_appointments_count}\
             <br> <a href='{self.reminder.href}title={self.subject_identifier} Note'>Add Note</a> ">
                {self.subject_identifier}
            </button>
        </div>
        '''

        return view

    def view_build(self):

        if self.is_child:
            return self._html('child_dashboard')
        else:
            return self._html('subject_dashboard')
