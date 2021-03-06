"""lamps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

import lampserver.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #url(r'^cmap/(?P<cmname>\w+)/(?<ncolorsteps>\d+)/(?<nmaps>\d+)', lampserver.views.cmap),
    url(r'^cmap/(?P<cmname>\w+)/(?P<alpha>[0-9]{1,3})/(?P<Nmaps>[0-9]{1,3})/(?P<Ncolorsteps>[0-9]{1,3})', lampserver.views.cmap,name='cmap_view'),
    url(r'^cmap/(?P<cmname>\w+)', lampserver.views.cmap, name='cmap_view'),
    url(r'^cmap', lampserver.views.cmap, name='cmap_view'),
    url(r'^rgb/(?P<R>[0-9]{1,3})/(?P<G>[0-9]{1,3})/(?P<B>[0-9]{1,3})/(?P<A>[0-9]{1,3})', lampserver.views.lamp_view, name='rgb_view'),
    url(r'^rgb/get_lamp_colors', lampserver.views.get_lamp_colors, name='rgb_get_lamp_colors'),
    url(r'^rgb/', lampserver.views.lamp_view, name='rgb_view'),
    url(r'^$', lampserver.views.lamp_view),
]
