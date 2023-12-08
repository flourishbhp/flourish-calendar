from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from flourish_calendar.utils import ReminderDuplicator
from .reminder_model import Reminder


@receiver(post_save, sender=Reminder)
def reminder_post_save(sender, instance, created, **kwargs):
    if instance.pk is None or instance.tracker.has_changed(
            'repeat') or instance.tracker.has_changed(
            'start_date') or instance.tracker.has_changed(
            'end_date') or instance.tracker.has_changed('remainder_time'):
        reminder_duplicator = ReminderDuplicator(instance)
        reminder_duplicator.remove_duplicates()  # Method to remove duplicates
        reminder_duplicator.repeat()


@receiver(pre_save, sender=Reminder)
def reminder_pre_save(sender, instance, **kwargs):
    if instance.pk is not None:
        Reminder.objects.filter(title=Reminder.objects.get(id=instance.id).title).delete()
