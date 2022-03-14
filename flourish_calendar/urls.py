
from django.urls import path
from . import views
from .admin_site import flourish_calendar_admin
app_name = 'flourish_calendar'
app_label = 'flourish_calendar'

urlpatterns = [
    path('admin/', flourish_calendar_admin.urls),

    path('', views.CalendarView.as_view(), name='calendar'),
]
