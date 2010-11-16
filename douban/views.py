# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from douban.models import Post, Segment
from django.views.generic.list_detail import object_list

def post(request, slug):
	segments = Segment.objects.all()
	return object_list(request, template_name='post.html', queryset=segments)