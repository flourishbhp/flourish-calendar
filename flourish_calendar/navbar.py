from django.conf import settings
from edc_navbar import NavbarItem, site_navbars, Navbar


flourish_calendar = Navbar(name='flourish_calendar')


site_navbars.register(flourish_calendar)
