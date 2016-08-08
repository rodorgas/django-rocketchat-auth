from django.conf.urls import url
from rocketchat_auth import views


urlpatterns = [
    url(r'^$', views.home),
    url(r'^api$', views.api),
    url(r'^redirect$', views.redirect_rocketchat),
]
