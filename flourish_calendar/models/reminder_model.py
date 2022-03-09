import imp
from pydoc import describe
from statistics import mode
from edc_base.model_mixins import BaseUuidModel
from django.db import models
from edc_constants.choices import YES_NO

class Reminder(BaseUuidModel):
    title = models.CharField(max_length=50)
    subject_identifier = models.CharField(max_length=20)
    datetime = models.DateTimeField()
    description = models.TextField(blank=True, null=True)
    completed = models.CharField(max_length=3, choices=YES_NO, blank=True, null=True)
