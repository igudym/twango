from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('core.twango.views',
        (r'^$','index'),
)
