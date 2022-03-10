from ..models import Reminder
from ..model_wrappers import ReminderModelWrapper

class ReminderHtmlBuilder:
    def __init__(self, reminder: Reminder) -> None:
        self._reminder = reminder 
    
    def _html(self):
        view = "<div class='item'><li>"

        reminder_wrapper = ReminderModelWrapper(model_obj=self._reminder)

        view += f"""\
            <a target="__blank" href="{reminder_wrapper.href}">
                <b>{self._reminder.title}</b>
            </a>
                <br/>
                Completed : {self._reminder.status.replace('-', ' ').title()}
                <br/>
            """

        view += "</li></div>"

        return view

    def view_build(self):
        return self._html()
