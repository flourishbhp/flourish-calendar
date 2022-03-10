from ..models import Reminder
from ..model_wrappers import ReminderModelWrapper

class ReminderHtmlBuilder:
    def __init__(self, reminder: Reminder) -> None:
        self._reminder = reminder 

    @property
    def status(self):
        return self._reminder.status.replace("_", " ").title()
    
    def _html(self):
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

    def view_build(self):
        return self._html()
