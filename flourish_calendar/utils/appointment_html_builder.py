import imp
from django.apps import apps as django_apps
from edc_appointment.models import Appointment
from ..model_wrappers import ReminderModelWrapper, ParticipantNoteModelWrapper
from ..models import Reminder, AppointmentStatus, ParticipantNote
from ..choices import APPT_COLOR
from django.template.loader import render_to_string

from edc_appointment.choices import (
    NEW_APPT,
    IN_PROGRESS_APPT,
    INCOMPLETE_APPT,
    COMPLETE_APPT,
    CANCELLED_APPT
)


class AppointmentHtmlBuilder:
    child_appointment_model = 'flourish_child.appointment'

    def __init__(self, appointment: Appointment, request) -> None:
        self._appointment = appointment
        self._subject_identifier = self._appointment.subject_identifier
        self.request = request

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
        
        # ('green', 'red', 'grey', 'yellow')
        
        status = None
        
        try:
            appt = AppointmentStatus.objects.get(subject_identifier=self.subject_identifier)
        except AppointmentStatus.DoesNotExist:
            pass
        else:
            if appt.color == 'green':
                status =  'label-success'
            elif appt.color == 'red':
                status = 'label-danger'
            elif appt.color == 'grey':
                status = 'label-default'
            elif appt.color == 'yellow':
                status =  'label-warning'
            
        return status

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
    def participant_note_wrapper(self):
        participent_note = ParticipantNote()
        return ParticipantNoteModelWrapper(model_obj=participent_note)
    
    @property
    def appointment_choices(self):
        colors = ('green', 'red', 'yellow')
        
        color_dictionary = zip(colors, dict(APPT_COLOR).values())
    
        return color_dictionary

    @property
    def add_reschedule_reason(self):
        # if self.resceduled_appointments_count:
        return f'''<br> <a href='{self.participant_note_wrapper.href}title = {self.subject_identifier} - Rescedule reason'></a> '''

    def _html(self, dashboard_type):
        icon = None
        if 'quart' in self._appointment.schedule_name:
            icon = '📞'
        else:
            icon = '👩'
        view = render_to_string('flourish_calendar/appointment_template.html', {
            'status_color': self.status_color,
            'dashboard_type': dashboard_type,
            'subject_identifier': self.subject_identifier,
            'visit_code': self.visit_code,
            'status': self.status,
            'resceduled_appointments_count': self.resceduled_appointments_count,
            'participant_note_wrapper': self.participant_note_wrapper,
            'icon': icon,
            'appointment_choices': self.appointment_choices,
            'date': self._appointment.appt_datetime.date().isoformat()
        }, request=self.request)
        

        return view

    def view_build(self):

        if self.is_child:
            return self._html('child_dashboard')
        else:
            return self._html('subject_dashboard')
