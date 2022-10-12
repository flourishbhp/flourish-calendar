
from django.db import models
from django.forms import ValidationError
from django.utils import timezone
from edc_base.model_mixins import BaseUuidModel
from ..choices import COLORS, REMINDER_STATUS


class ParticipantNote(BaseUuidModel):
    date = models.DateField()
    subject_identifier = models.CharField(
        max_length=19)
    title = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=20, blank=True, null=True, choices=COLORS)

    class Meta(BaseUuidModel.Meta):
        app_label = 'flourish_calendar'
        verbose_name = 'Participant Note'
