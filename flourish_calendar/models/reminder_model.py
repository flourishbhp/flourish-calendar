import django.utils.timezone
from django.db import models
from edc_base.model_mixins import BaseUuidModel

from ..choices import COLORS, REPEAT


class Reminder(BaseUuidModel):
    datetime = models.DateTimeField(default=django.utils.timezone.now)

    title = models.CharField(max_length=70)

    start_date = models.DateField()

    end_date = models.DateField()

    remainder_time = models.TimeField()

    note = models.TextField(blank=True, null=True)

    color = models.CharField(max_length=20,
                             blank=True,
                             null=True,
                             choices=COLORS)

    repeat = models.CharField(
        default=None,
        null=True,
        blank=True,
        choices=REPEAT,
        max_length=10
    )

    @property
    def is_repeated(self):
        return Reminder.objects.filter(
            title=self.title,
            note=self.note,
            repeat=self.repeat).count() > 1

    class Meta(BaseUuidModel.Meta):
        app_label = 'flourish_calendar'
        verbose_name = 'Note'
