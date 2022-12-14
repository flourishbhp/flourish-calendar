from email.policy import default
from tabnanny import verbose
from edc_base.model_mixins import BaseUuidModel
from django.db import models
from django.utils import timezone
from ..choices import COLORS

class Reminder(BaseUuidModel):
    title = models.CharField(max_length=70)
    datetime = models.DateTimeField()
    note = models.TextField(blank=True, null=True)

    color = models.CharField(max_length=20,
                             blank=True,
                             null=True,
                             choices=COLORS)

    @property
    def date(self):
        return self.datetime.date()

    class Meta(BaseUuidModel.Meta):
        app_label = 'flourish_calendar'
        verbose_name = 'Note'
