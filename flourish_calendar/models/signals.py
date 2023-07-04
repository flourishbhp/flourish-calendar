from flourish_calendar.utils import ReminderDuplicator
from django.db.models.signals import post_save
from django.dispatch import receiver
from .reminder_model import Reminder

@receiver(post_save, sender=Reminder)
def reminder_post_save(sender, instance, created, **kwargs):
    if instance and not instance.is_repeated:
        duplicator = ReminderDuplicator(instance)
        duplicator.repeat()