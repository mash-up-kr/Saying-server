from django.conf.urls import url
from .views import register_user, update_profile, activate, acc_check


urlpatterns = [
    url(r'^check$', acc_check, name='check'),
    url(r'^register$', register_user, name='register'),
    url(r'^activate/(?P<userid>[^/]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),
    url(r'^profile$', update_profile, name='profile'),
]