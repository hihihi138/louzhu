from django.contrib import admin
from douban.models import Post, Segment

class PostAdmin(admin.ModelAdmin):
	list_display = ('name', 'author', 'post_date', 'slug', 'url')
	search_fields = ('name', 'author',)
	list_filter = ('post_date',)
	date_hierarchy = 'post_date'

admin.site.register(Post, PostAdmin)
admin.site.register(Segment)