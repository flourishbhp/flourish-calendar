from edc_model_wrapper import ModelWrapper
from django.apps import apps as django_apps
from django.conf import settings

class ReminderModelWrapper(ModelWrapper):
    model = "flourish_calendar.reminder"
    next_url_name = settings.DASHBOARD_URL_NAMES.get('flourish_calendar_url')