from django.conf.urls import url
from django.urls import path
from django.views.generic import TemplateView
from .views import  Forecast

urlpatterns = [
    path('<str:type>/<str:location>/<str:horizon>/', Forecast.as_view(), name='modelpreds'),
]
