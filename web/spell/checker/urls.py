from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='checker.index'),
    url(r'^stats$', views.stats, name='checker.stats'),
]
