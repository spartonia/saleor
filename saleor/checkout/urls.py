from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.details, kwargs={'step': None}, name='index'),
    url(r'^update_details/(?P<which_service>\d+)/$', views.update_details, name='update_details'),
    url(r'^(?P<step>[a-z0-9-]+)/$', views.details, name='details'),
]
