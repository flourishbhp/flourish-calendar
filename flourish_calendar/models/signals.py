from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from flourish_calendar.utils import ReminderDuplicator
from .reminder_model import Reminder


@receiver(pre_save, sender=Reminder)
def reminder_pre_save(sender, instance, *args, **kwargs):
    Reminder.objects.filter(
        title=instance.title,
        note=instance.note, ).delete()


@receiver(post_save, sender=Reminder)
def reminder_post_save(sender, instance, created, **kwargs):
    ReminderDuplicator(instance).repeat()
