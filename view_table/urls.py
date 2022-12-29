from django.urls import path
from . import views
from django.views.generic.base import RedirectView
from view_table.dash_apps.finished_apps import table

urlpatterns = [
    path('', views.table, name='table'),
    path('admin', RedirectView.as_view(url='/admin')),
    path('home', RedirectView.as_view(url=' '))]