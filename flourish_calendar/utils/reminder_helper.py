import datetime

from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from django.forms import model_to_dict

from ..constants import DAILY, MONTHLY, WEEKLY, YEARLY, ONCE
from ..models import Reminder


class WorkingDays:
    holiday_model = 'edc_facility.holiday'

    def holiday(self, day):
        return django_apps.get_model(self.holiday_model).objects.filter(
            local_date=day).exists()

    def is_valid_working_day(self, day):
        return day.weekday() < 5 and not self.holiday(day)


class ReminderDuplicator(WorkingDays):
    def __init__(self, reminder: Reminder):
        self.reminder = reminder
        self.validation_of_days = {
            ONCE: relativedelta(days=0),
            DAILY: datetime.timedelta(days=1),
            WEEKLY: datetime.timedelta(days=7),
            MONTHLY: relativedelta(months=1),
            YEARLY: relativedelta(years=1)
        }

    def repeat(self):
        dates = self._get_dates_based_on_recurrence()
        reminders = [self._create_new_reminder(date) for date in dates]
        Reminder.objects.bulk_create(reminders)

    def _get_dates_based_on_recurrence(self):
        return [date for date in self._generate_potential_dates() if
                self.is_valid_working_day(date)]

    def _generate_potential_dates(self):
        date_series = []

        start_date = self.reminder.start_date
        end_date = self.reminder.end_date
        repeat = self.reminder.repeat or ONCE  # for backward compatibility

        date_increment_value = self.validation_of_days[repeat]

        if repeat == ONCE:
            date_series.append(start_date)
        else:
            while start_date <= end_date:
                date_series.append(start_date)
                start_date += date_increment_value

        return date_series

    def _create_new_reminder(self, date):
        reminder_dict = model_to_dict(self.reminder)
        datetime_object = datetime.datetime.combine(date, self.reminder.remainder_time)
        reminder_dict.update({'datetime': datetime_object})
        return Reminder(**reminder_dict)


    def remove_duplicates(self):
        unique_reminders = Reminder.objects.filter(
            title=self.reminder.title,
            note=self.reminder.note,
            repeat=self.reminder.repeat
        ).values('title', 'note', 'repeat').distinct()

        for unique_reminder in unique_reminders:
            duplicate_reminders = Reminder.objects.filter(**unique_reminder)

            first_reminder = duplicate_reminders.first()
            if first_reminder:
                duplicate_reminders = duplicate_reminders.exclude(pk=first_reminder.pk)

            if duplicate_reminders.exists():
                duplicate_reminders.delete()
