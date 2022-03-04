import calendar


from datetime import datetime, date, timedelta
from urllib import request
from django.views import generic
from django.utils.safestring import mark_safe
from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin
from edc_appointment.models import Appointment
from .utils import Calendar

class CalendarView(NavbarViewMixin, EdcBaseViewMixin, generic.ListView):

    navbar_name = 'flourish_calendar'
    navbar_selected_item = 'calendar'
    model = Appointment
    template_name = 'flourish_calendar/templates/flourish_calendar/calendar.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('month', None))

        if self.request.GET.get('filter', None):        
            self.request.session['filter'] = self.request.GET.get('filter', None)




        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month, self.request.session.get('filter', None))

        # Call the formatmonth method, which returns our calendar as a table

        html_cal = cal.formatmonth(withyear=True)

        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        context['calendar'] = mark_safe(html_cal)
        context['filter'] = self.request.session.get('filter', None)
        return context


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month
