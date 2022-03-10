import imp
from pydoc import describe
from statistics import mode
from tabnanny import verbose
from edc_base.model_mixins import BaseUuidModel
from django.db import models
from edc_appointment.choices import APPT_STATUS

class Reminder(BaseUuidModel):
    title = models.CharField(max_length=20)
    datetime = models.DateTimeField()
    note = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=29, choices=APPT_STATUS, blank=True, null=True)

    class Meta(BaseUuidModel.Meta):
        app_label = 'flourish_calendar'
        verbose_name = 'Reminder'
