
import imp
from django.urls import path
from . import views

app_name = 'calendar_dashboard'
urlpatterns = [
    path('', views.CalendarView.as_view(), name='calendar'),
]
