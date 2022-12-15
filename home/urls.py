from django.urls import path
from . import views
from home.dash_apps.finished_apps import simpleexample, time_series_dash

urlpatterns = [
    path('', views.home, name='home')]