from .constants import DAILY, WEEKLY, MONTHLY, WEEKDAYS, YEARLY

NOTE_TYPE = (
    ('general_note', 'General Note'),
    ('reminder_note', 'Reminder Note'),
    ('reschedule_note', 'Reschedule Note'),
)


APPT_COLOR = (
    ('done', 'Done'),  # green
    ('cancelled', 'Cancelled'),  # red
    ('recall', 'Recall'),  # yellow
)

REMINDER_STATUS = (
    ('done', 'Done'),
    ('new', 'New')
)

COLORS = (
    ('green', 'Green'),
    ('red', 'Red'),
    ('grey', 'Grey'),
    ('yellow', 'Yellow'),
    ('purple', 'Purple'),
    ('pink', 'Pink'),
    ('blue', 'Blue'),
    ('teal', 'Teal'),
    ('black', 'Black')
)

REPEAT = (
    (DAILY, 'Daily'),
    (WEEKLY, 'Weekly'),
    (MONTHLY, 'Monthly'),
    (YEARLY, 'Yearly')
)
