from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from flourish_calendar.utils import ReminderDuplicator
from .reminder_model import Reminder


@receiver(post_save, sender=Reminder)
def reminder_post_save(sender, instance, created, **kwargs):
    if created:
        ReminderDuplicator(instance).repeat()
    else:
        historical_instance = instance.history.all()
        if not historical_instance:
            return
        ReminderDuplicator(instance).remove_duplicates(historical_instance)
        ReminderDuplicator(instance).repeat()


