
import imp
from django.urls import path
from . import views

app_name = 'flourish_calendar'
urlpatterns = [
    path('', views.CalendarView.as_view(), name='calendar'),
]
