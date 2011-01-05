from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^louzhu/', include('louzhu.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

	(r'^$', 'views.main'),
	#(r'^http://www.douban.com/group/topic/', include('douban.urls')),
	#(r'^www.douban.com/group/topic/', include('douban.urls')),
	(r'^(.*)douban.com/group/topic/', include('douban.urls')),
	(r'^group/topic/', include('douban.urls')),
	(r'^douban/', include('douban.urls')),
	
	# static files
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
