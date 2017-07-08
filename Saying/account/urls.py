from django.conf.urls import url
from .views import start


urlpatterns = [
    url(r'^$', start, name='start'),
]