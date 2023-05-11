from edc_base.model_mixins import BaseUuidModel
from django.db import models
from ..choices import COLORS, REPEAT

class Reminder(BaseUuidModel):
    title = models.CharField(max_length=70)
    datetime = models.DateTimeField()
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

    @property
    def date(self):
        return self.datetime.date()

    class Meta(BaseUuidModel.Meta):
        app_label = 'flourish_calendar'
        verbose_name = 'Note'
