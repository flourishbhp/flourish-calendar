from email.policy import default
from tabnanny import verbose
from edc_base.model_mixins import BaseUuidModel
from django.db import models
from django.utils import timezone
from ..choices import NOTE_TYPE, REMINDER_STATUS

class Reminder(BaseUuidModel):
    title = models.CharField(max_length=20)
    type = models.CharField(choices=NOTE_TYPE, max_length=20)
    status =  models.CharField(choices=REMINDER_STATUS, max_length=20)
    datetime = models.DateTimeField()
    note = models.TextField(blank=True, null=True)

    class Meta(BaseUuidModel.Meta):
        app_label = 'flourish_calendar'
        verbose_name = 'Note'
