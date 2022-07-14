from email.policy import default
from tabnanny import verbose
from edc_base.model_mixins import BaseUuidModel
from django.db import models
from django.utils import timezone

class Reminder(BaseUuidModel):
    title = models.CharField(max_length=20)
    datetime = models.DateTimeField()
    note = models.TextField(blank=True, null=True)

    class Meta(BaseUuidModel.Meta):
        app_label = 'flourish_calendar'
        verbose_name = 'Note'
