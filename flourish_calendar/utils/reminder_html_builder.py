from tkinter import SEL_LAST
from typing import Any
from ..models import Reminder, ParticipantNote
from ..model_wrappers import ReminderModelWrapper, ParticipantNoteModelWrapper
from django.template.loader import render_to_string

class ReminderHtmlBuilder:
    def __init__(self, reminder: Any) -> None:
        self._reminder = reminder 

    @property
    def status(self):
        return self._reminder.status.replace("_", " ").title()
    
    def _reminder_html(self):
        view = "<div class='item'><li>"

        reminder_wrapper = ReminderModelWrapper(model_obj=self._reminder)

        view += f"""\
            <a target="__blank" href="{reminder_wrapper.href}">
                <b>{self._reminder.title}</b>
            </a>
            """

        if self._reminder.status:
            view += f"""\
                <br/>
                Status : {self.status}
                <br/>
                """
        else:
            view += f"""\
                <br/>
                Status : Not Set
                <br/>
                """


        view += "</li></div>"

        return view
    
    @property
    def status_color(self):
        
        # ('green', 'red', 'grey', 'yellow')
        status = None
        
        if self._reminder.color == 'green':
            status =  'label-success'
        elif self._reminder.color == 'red':
            status = 'label-danger'
        elif self._reminder.color == 'grey':
            status = 'label-default'
        elif self._reminder.color == 'yellow':
            status =  'label-warning'
            
        return status
    
    def _participant_notes_html(self):
        view = "<div class='item participant_notes'><li>"

        participant_note_wrapper = ParticipantNoteModelWrapper(model_obj=self._reminder)
        icon = '📝'
        
        if "Follow" in self._reminder.title:
            icon = '➡️'

        
        return render_to_string('flourish_calendar/follow_appointment_template.html', {
            # 'status_color': self.status_color,
            # 'dashboard_type': dashboard_type,
            'subject_identifier': self._reminder.subject_identifier,
            'link': participant_note_wrapper.href,
            'icon': icon,
            'note': self._reminder.description,
            'color': self._reminder.color,
            'status_color' : self.status_color
            
        })

    def view_build(self):

        if type(self._reminder) is Reminder:
            return self._reminder_html()
        elif type(self._reminder) is ParticipantNote:
            return self._participant_notes_html()