from django.conf import settings
from edc_navbar import NavbarItem, site_navbars, Navbar


flourish_calendar = Navbar(name='flourish_calendar')

no_url_namespace = True if settings.APP_NAME == 'flourish_calendar' else False


flourish_calendar.append_item(
    NavbarItem(
        name='calendar',
        label='Calendar',
        fa_icon='far fa-calendar',
        url_name='flourish_calendar:calendar'))


site_navbars.register(flourish_calendar)
