import django.utils.timezone
from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_protocol.validators import date_not_before_study_start

from ..choices import COLORS, REPEAT


class Reminder(BaseUuidModel):
    datetime = models.DateTimeField(blank=True, null=True)

    title = models.CharField(max_length=70)

    start_date = models.DateField(
        validators=[
            date_not_before_study_start],

    )

    end_date = models.DateField(
        blank=True,
        null=True,
        validators=[
            date_not_before_study_start],
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

    @property
    def date(self):
        if self.datetime:
            return self.datetime.date()
        else:
            return None

    class Meta(BaseUuidModel.Meta):
        app_label = 'flourish_calendar'
        verbose_name = 'Note'
