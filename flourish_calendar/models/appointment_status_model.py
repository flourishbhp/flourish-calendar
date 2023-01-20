from django.db import models
from edc_base.model_mixins import BaseUuidModel
from ..choices import APPT_COLOR

class AppointmentStatus(BaseUuidModel):
    '''
    Model for keeping track of appointment colors based on the subject identifier
    and visit code
    '''
    subject_identifier = models.CharField(max_length=20)
    visit_code = models.CharField(max_length=10)
    color = models.CharField(max_length=10, choices=APPT_COLOR)
    appt_date = models.DateTimeField()