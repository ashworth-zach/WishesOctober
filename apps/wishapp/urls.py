from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^process$', views.add), 
    url(r'^login$', views.login),
    url(r'^wishes$',views.wishes),
    url(r'^wishes/new$',views.new),
    url(r'^wishes/new/add$',views.wishadd),
    url(r'^wishes/grant/(?P<wishid>\d+)$',views.grantwish),
    url(r'^wishes/edit/(?P<wishid>\d+)$',views.editwish),
    url(r'^wishes/update/(?P<wishid>\d+)$',views.updatewish),
    url(r'^wishes/remove/(?P<wishid>\d+)$',views.delete),
    url(r'^logout$',views.logout),
    url(r'^wishes/stats$',views.stats),
    url(r'^like/(?P<wishid>\d+)/(?P<userid>\d+)$', views.like)


]  