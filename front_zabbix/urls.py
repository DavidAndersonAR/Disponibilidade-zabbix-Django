"""
URL configuration for front_zabbix project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from zabbix.views import index, hosts_por_grupo, obter_hosts_por_grupo

urlpatterns = [
    path("zabbix/", include("zabbix.urls")),
    path('admin/', admin.site.urls),
    path("index/", index, name="index" ),
    #path("hosts/", obter_hosts, name="obter_hosts" ),
    path('', hosts_por_grupo, name='hosts_por_grupo'),
    path('api/obter_hosts_por_grupo/<str:grupo>/', obter_hosts_por_grupo, name='obter_hosts_por_grupo'),
]
