from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

user_list = UserViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve',
})

urlpatterns = format_suffix_patterns([
    url(r'^register$', register_user, name='register'),
    url(r'^activate/(?P<userid>[^/]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),
    url(r'^profile$', update_profile, name='profile'),
    url(r'^users/$', user_list, name='user-list'),
    url(r'^users/(?P<pk>[^/]+)/$', user_detail, name='user-detail'),
])
