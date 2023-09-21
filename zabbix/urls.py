from django.urls import path
from . import views


urlpatterns = [
    path("index/", views.index, name="index"),
    #path("hosts/", views.obter_hosts, name="obter_hosts"),
]