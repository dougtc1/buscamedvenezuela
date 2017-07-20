from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^$', views.goHome, name='goHome'),
    url(r'^tweetsOferta/$', views.buscaTweets, name='buscaTweets'),    
    url(r'^tweetsDemanda/$', views.buscaTweets, name='buscaTweets'),
    url(r'^search/?$', views.searchFamily, name='searchFamily'),
    url(r'^lista/$', views.lista, name='lista'),
]