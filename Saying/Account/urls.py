from django.conf.urls import url
from .views import register_user, update_profile


urlpatterns = [
    url(r'^register$', register_user, name='register'),
    url(r'^profile$', update_profile, name='profile'),
]