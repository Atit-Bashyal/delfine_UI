from django.urls import path
from . import views
from django.views.generic.base import RedirectView
from view_graph.dash_apps.finished_apps import timeseries

urlpatterns = [
    path('', views.chart, name='chart'),
    path('admin', RedirectView.as_view(url='/admin')),
    path('home', RedirectView.as_view(url=' '))]