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
        view = None

        if self.status_color:
            view = f"<div class='item {self.status_color}'><li>"
        else:
            view = f"<div class='item'><li>"
        reminder_wrapper = ReminderModelWrapper(model_obj=self._reminder)

        view += f"""\
            <a target="__blank" href="{reminder_wrapper.href}" class="{f'colored {self.status_color}' if self.status_color else None}">
                <b>{self._reminder.title}</b>
            </a>
            """
        view += "</li></div>"

        return view

    @property
    def status_color(self):

        status = None

        if self._reminder.color == 'green':
            status = 'label-success'
        elif self._reminder.color == 'red':
            status = 'label-danger'
        elif self._reminder.color == 'grey':
            status = 'label-default'
        elif self._reminder.color == 'yellow':
            status = 'label-warning'

        elif self._reminder.color in \
                ('purple', 'blue', 'pink', 'teal', 'black'):
            status = self._reminder.color

        return status

    @property
    def _dashboard_type(self):
        if len(self._reminder.subject_identifier) == 16:
            return 'subject_dashboard'
        else:
            return 'child_dashboard'

    @property
    def new_participant_note_wrapper(self):
        participent_note = ParticipantNote()
        return ParticipantNoteModelWrapper(model_obj=participent_note)

    def _participant_notes_html(self):
        participant_note_wrapper = ParticipantNoteModelWrapper(model_obj=self._reminder)
        icon = '📝'

        if "Follow" in self._reminder.title:
            icon = '➡️'

        return render_to_string('flourish_calendar/follow_appointment_template.html', {
            # 'status_color': self.status_color,
            # 'dashboard_type': dashboard_type,
            'subject_identifier': self._reminder.subject_identifier,
            'participant_note_wrapper': participant_note_wrapper,
            'new_participant_note_wrapper': self.new_participant_note_wrapper,
            'icon': icon,
            'note': self._reminder.description,
            'color': self._reminder.color,
            'date': self._reminder.date,
            'status_color': self.status_color,
            'dashboard_type': self._dashboard_type,
            'cohort': getattr(participant_note_wrapper, 'cohort', None)
        })

    def view_build(self):
        if type(self._reminder) is Reminder:
            return self._reminder_html()
        elif type(self._reminder) is ParticipantNote:
            return self._participant_notes_html()
