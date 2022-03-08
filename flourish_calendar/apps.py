from django.apps import AppConfig as DjangoApponfig


class AppConfig(DjangoApponfig):
    name = 'flourish_calendar'
    app_name = 'flourish_calendar'
    app_label = 'flourish_calendar'
    verbose_name = 'Flourish Calendar'
    extra_assignee_choices = ()
    assignable_users_group = 'assignable users'
