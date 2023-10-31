import django.utils.timezone
from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import date_not_future
from edc_protocol.validators import date_not_before_study_start

from ..choices import COLORS, REPEAT


class Reminder(BaseUuidModel):
    datetime = models.DateTimeField(default=django.utils.timezone.now)

    title = models.CharField(max_length=70)

    start_date = models.DateField(
        validators=[
            date_not_before_study_start,
            date_not_future],

    )

    end_date = models.DateField(
        validators=[
            date_not_before_study_start,
            date_not_future],
    )

    remainder_time = models.TimeField()

    note = models.TextField(blank=True, null=True)

    color = models.CharField(max_length=20,
                             choices=COLORS)

    repeat = models.CharField(
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
