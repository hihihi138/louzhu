# -*-coding:utf-8 -*-
from django.db import models
from datetime import datetime

class Post(models.Model):
	name = models.CharField(max_length=100, verbose_name='帖子标题')
	url = models.URLField(verbose_name='豆瓣原址')
	author = models.CharField(max_length=30, verbose_name='楼主大名')
	author_url = models.URLField(verbose_name='楼主豆瓣')
	post_date = models.DateTimeField(default=datetime.now(), verbose_name='建立时间')
	last_date = models.DateTimeField(verbose_name='最后更新')
	intro = models.TextField(max_length=4096, blank=True, verbose_name='帖子简介')
	slug = models.SlugField(max_length=15)
	
	def get_absolute_url(self):
		return '/%s/' % self.slug
        
	def __unicode__(self):
		return self.name
		
	class Meta:
		ordering = ['-post_date']
        
class Segment(models.Model):
	post = models.ForeignKey(Post, verbose_name='帖子')
	date = models.DateTimeField(verbose_name='发表时间')
	content = models.TextField(max_length=4096, verbose_name='楼层内容')
	
	def __unicode__(self):
		return self.post.name
	class Meta:
		ordering = ['-date']