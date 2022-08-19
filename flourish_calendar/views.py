from django.utils.safestring import mark_safe
from django.views import generic
from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin

from edc_appointment.models import Appointment

from .model_wrappers import ReminderModelWrapper, ParticipantNoteModelWrapper
from .models import Reminder, ParticipantNote
from .utils import AppointmentHelper
from .utils import DateHelper, CustomCalendar


class CalendarView(NavbarViewMixin, EdcBaseViewMixin, generic.ListView):
    navbar_name = 'flourish_calendar'
    navbar_selected_item = 'calendar'
    model = Appointment
    template_name = 'flourish_calendar/calendar.html'

    @property
    def new_reminder_wrapper(self):
        reminder = Reminder()
        reminder_wrapper = ReminderModelWrapper(model_obj=reminder)
        return reminder_wrapper

    @property
    def new_participant_wrapper(self):
        participant_note = ParticipantNote()
        participant_note_wrapper = ParticipantNoteModelWrapper(
            model_obj=participant_note
        )
        return participant_note_wrapper

    def get(self, request, *args, **kwargs):

        subject_identifier = request.GET.get('subject_identifier', None)
        visit_code = request.GET.get('visit_code', None)
        color = request.GET.get('choice', None)
        date = request.GET.get('date', None)

        AppointmentHelper.change_color(
            subject_identifier=subject_identifier,
            visit_code=visit_code,
            color=color,
            appt_date=date
        )

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        month = self.request.GET.get('month', None)

        # use today's date for the calendar
        d = DateHelper.get_date(month)

        search_filter = self.request.GET.get('filter', "")
        search_term = self.request.GET.get('search_term', None)

        if search_filter != self.request.session.get('filter', 'not-the-same-placeholder'):
            self.request.session['filter'] = search_filter

        if search_term != self.request.session.get('search_term', 'not-the-same-placeholder'):
            self.request.session['search_term'] = search_term

        # Instantiate our calendar class with today's year and date
        cal = CustomCalendar(d.year, d.month, self.request)

        # Call the formatmonth method, which returns our calendar as a table

        html_cal = cal.formatmonth(withyear=True)

        context.update(
            prev_month=DateHelper.prev_month(d),
            next_month=DateHelper.next_month(d),
            calendar=mark_safe(html_cal),
            filter=self.request.session.get('filter', None),
            search_term=self.request.session.get('search_term', ''),
            new_reminder_url=self.new_reminder_wrapper.href,
            new_participant_note_url=self.new_participant_wrapper.href)

        return context
