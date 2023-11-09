from .constants import ONCE, DAILY, WEEKLY, MONTHLY, WEEKDAYS, YEARLY

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
    ('green', 'Green - Done'),
    ('red', 'Red - Missed/Canceled appointment'),
    ('grey', 'Grey'),
    ('yellow', 'Yellow - Recalls'),
    ('purple', 'Purple - Home visits'),
    ('pink', 'Pink - Clinic updates'),
    ('blue', 'Blue - Pick ups'),
    ('teal', 'Teal - Leaves: Annual/Sick'),
    ('black', 'Black')
)

REPEAT = (
    (ONCE, 'Once'),
    (DAILY, 'Daily'),
    (WEEKLY, 'Weekly'),
    (MONTHLY, 'Monthly'),
    (YEARLY, 'Yearly')
)
