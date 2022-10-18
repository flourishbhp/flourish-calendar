from django.db import models
from edc_base.model_mixins import BaseUuidModel

from ..choices import COLORS


class ParticipantNote(BaseUuidModel):

    date = models.DateField()

    subject_identifier = models.CharField(max_length=25)

    title = models.CharField(max_length=20,
                             # default='Follow Up Schedule'
                             )

    description = models.TextField(blank=True,
                                   null=True)

    color = models.CharField(max_length=20,
                             blank=True,
                             null=True,
                             choices=COLORS)

    class Meta(BaseUuidModel.Meta):
        app_label = 'flourish_calendar'
        verbose_name = 'Participant Note'
