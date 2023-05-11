
import calendar
import datetime
from django.forms import model_to_dict
from django.apps import apps as django_apps
from ..constants import DAILY, WEEKLY, MONTHLY, WEEKDAYS, YEARLY
from ..models import Reminder


class ReminderDuplicator:

    holiday_model = 'edc_facility.holiday'

    def __init__(self, reminder):
        self.reminder = reminder

    @property
    def holiday_cls(self):
        return django_apps.get_model(self.holiday_model)

    def is_holiday(self, date):
        return self.holiday_cls.objects.filter(
            local_date=date
        ).exists()

    def repeat(self):

        reminder_date = self.reminder.date
        dates = []
        reminders = []

        if self.reminder.repeat == DAILY:
            dates = self._get_working_days(
                reminder_date.year, reminder_date.month)
        elif self.reminder.repeat == WEEKLY:
            pass
        elif self.reminder.repeat == MONTHLY:
            pass
        elif self.reminder.repeat == YEARLY:
            pass
        else:
            pass

        for date in dates:

            if date <= self.reminder.date or self.is_holiday(date):
                continue

            reminder_dict = model_to_dict(self.reminder)
            reminder_dict['datetime'] = datetime.datetime.combine(
                date, self.reminder.datetime.time())

            reminders.append(Reminder(**reminder_dict))

        Reminder.objects.bulk_create(reminders)

    def _get_working_days(self, year, month):
        # get total number of days in the month
        num_days = calendar.monthrange(year, month)[1]

        # loop through all days in the month
        working_days = []
        for day in range(1, num_days+1):
            date = datetime.date(year, month, day)
            # check if the day is a weekday (0 = Monday, 6 = Sunday)
            if date.weekday() < 5:
                working_days.append(date)

        # return the list of working days
        return working_days
