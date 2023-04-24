
import calendar
from datetime import date, timedelta, datetime
from django.forms import model_to_dict
from ..constants import DAILY, WEEKLY, MONTHLY, WEEKDAYS
from ..models import Reminder

class ReminderHelper:
    
    
    
    @staticmethod
    def repeat(reminder: Reminder):
        
        repeat_types = [DAILY, WEEKLY, MONTHLY, WEEKDAYS]
        
        type = reminder.repeat
        
        if type not in repeat_types:
            raise Exception('Repeat type not valid')
        
        days = []
        
        if reminder:
            if type == DAILY:
                days =  ReminderHelper._get_workdays_in_month(reminder.date.year, 
                                                   reminder.date.month)
            elif type == WEEKLY:
                days = ReminderHelper._get_week_day_in_a_month(reminder.date.year,
                                              reminder.date.month,
                                              reminder.date.strftime('%A'))
            elif type == MONTHLY:
                days = ReminderHelper._get_day_per_month(
                    reminder.date.year,
                    reminder.date.month,
                )
                
        days = filter(lambda element: element > reminder.date, days)

                
        for day in days:
            
            reminders_exist =Reminder.objects.filter(
                    datetime__date = day,
                    title = reminder.title,
                    note = reminder.note
                )
            
            if not reminders_exist.exists():
                
                reminder_dict = model_to_dict(reminder)
                reminder_dict['datetime'] = datetime.fromisoformat(day.isoformat())
                

                Reminder.objects.create(**reminder_dict)
                
                # reminder.datetime = day
                # reminder_dict = model_to_dict(reminder)            
                # Reminder.objects.create(
                #     **reminder_dict)

        
    def _get_workdays_in_month(year, month):
        # get the first day of the month
        date = datetime.date(year, month, 1)
    
        # iterate over all days in the month
        dates = []
        while date.month == month:
            # check if the current day is a weekday (0 = Monday, 6 = Sunday)
            if date.weekday() < 5:
                dates.append(date)
            date += datetime.timedelta(days=1)
            
        return dates
    
    
    def _get_week_day_in_a_month( year, month, weekday):
        # get the first day of the month
        date = datetime.date(year, month, 1)

        # find the first occurrence of the weekday in the month
        while date.weekday() != weekday:
            date += datetime.timedelta(days=1)

        # generate all the dates with the same weekday in the month
        dates = []
        while date.month == month:
            dates.append(date)
        date += datetime.timedelta(days=7)
        return dates
    
    def _get_day_per_month( year, day):
        months = []
        for month in range(1, 13):
            month_start = date(year, month, 1)
            month_end = date(year, month, calendar.monthrange(year, month)[1])
            for i in range((month_end - month_start).days + 1):
                curr_day = month_start + timedelta(days=i)
                if curr_day.strftime('%A') == day:
                    months.append(curr_day.strftime("%B %Y"))
                    break
        return months