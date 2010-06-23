from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'(?P<start_date>[-\w]+)/(?P<end_date>[-\w]+)/$', 'locationtracking.views.track'),
    (r'(?P<start_date>[-\w]+)/$', 'locationtracking.views.track'),
    (r'$', 'locationtracking.views.track'),
)
