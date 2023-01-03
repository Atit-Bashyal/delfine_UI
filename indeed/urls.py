from django.conf.urls import url
from django.urls import path
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin', RedirectView.as_view(url='/admin')),
    path('home', RedirectView.as_view(url=' '))
]
