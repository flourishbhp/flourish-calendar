from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from edc_model_wrapper import ModelWrapper


class ParticipantNoteModelWrapper(ModelWrapper):

    model = 'flourish_calendar.participantnote'
    querystring = ['title', ]
    next_url_name = settings.DASHBOARD_URL_NAMES.get('flourish_calendar_url')

    @property
    def title(self):
        return self.object.title
