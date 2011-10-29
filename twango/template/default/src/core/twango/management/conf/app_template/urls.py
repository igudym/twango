from django.conf.urls.defaults import *
from django.conf import settings

# You may have to replace 'views' with 'apps.(package).views below.'
# this is a known issue

urlpatterns = patterns('{{app_views_path}}',
        (r'^$','index'),
)
