from django.urls import path

from . import views
from .admin_site import flourish_calendar_admin
from .utils.export_helper import export_events_as_csv

app_name = 'flourish_calendar'
app_label = 'flourish_calendar'

urlpatterns = [
    path('admin/', flourish_calendar_admin.urls),
    path('export/', export_events_as_csv, name='export_calendar'),

    path('', views.CalendarView.as_view(), name='calendar'),
]
