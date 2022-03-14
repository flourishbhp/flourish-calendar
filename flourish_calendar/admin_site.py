
from django.contrib.admin import AdminSite as DjangoAdminSite


class AdminSite(DjangoAdminSite):

    site_title = 'Flourish Calendar'
    site_header = 'Flourish Calendar'
    index_title = 'Flourish Calendar'
    site_url = '/administration/'
    enable_nav_sidebar = False


flourish_calendar_admin = AdminSite(name='flourish_calendar_admin')
