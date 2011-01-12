from django.conf.urls.defaults import *

urlpatterns = patterns('douban.views',
	(r'^(\d+)', 'post'),
)