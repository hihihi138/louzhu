# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, redirect
from douban.models import Post, Segment
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.views.generic.list_detail import object_list
from django.core.exceptions import ObjectDoesNotExist
import urllib, re
from datetime import datetime
from django.views.decorators.cache import cache_page

#@cache_page(60 * 5)
def post(request, slug):
	path = '/douban/'+slug+'/'
	if request.path != (path):
		return redirect(path)
	try:
		post = Post.objects.get(slug=slug)
		print "The post is already in database."
	except ObjectDoesNotExist:
		print "New post, add it now."
		add_post(slug)
		post = Post.objects.get(slug=slug)
	page = get_segment(slug, post)
	if post.page != page:
		post.page = page
		post.save()
	segments = Segment.objects.filter(post=post)
	extra_context = {'name': post.name, 'url': post.url, 'author': post.author, 'author_url': post.author_url, 'dgroup': post.dgroup}
	return object_list(request, template_name='post.html', queryset=segments, paginate_by=50, extra_context=extra_context)
	
def add_post(slug):
	html = urllib.urlopen('http://www.douban.com/group/topic/'+slug)
	data = html.read()
	try:
		name = re.findall(r'<title>(.*?)</title>', data, re.S)[0].strip()
		url = html.url
		author = re.findall(r'<span class="pl20">.*?">(.*?)</a>', data, re.S)[0].strip()
		author_url = re.findall(r'<span class="pl20">.*?href="(.*?)">', data, re.S)[0].strip()
		d = re.findall(r'<span class="color-green">(.*?)</span>', data, re.S)[0]
		post_date = datetime.strptime(d, "%Y-%m-%d %H:%M:%S")
		last_date = datetime.now()
		dgroup = re.findall(r'/">回(.*)小组</a></p><br/>', data, re.S)[0]
		dgroup_url = re.findall(r'&gt; <a href="(.*)">回', data, re.S)[0]
		p = Post(name=name,url=url,author=author,author_url=author_url,post_date=post_date,last_date=last_date,slug=slug,page=0, dgroup=dgroup, dgroup_url=dgroup_url)
		p.save()
		content = re.findall(r'<p>(.*?)</p>', data, re.S)[0].strip()
		s = Segment(post = p, date = post_date, content = content)
		s.save()
	except IndexError:
		return "There is something wrong when parsing the page."

def get_segment(slug, post):
	url = 'http://www.douban.com/group/topic/'+slug+'/?start='+str(post.page)
	html = urllib.urlopen(url)
	data = html.read()
	author = post.author.encode('UTF-8')
	page = post.page
	print "start from:"
	print url
	parse_segment(data, post, author)
	try:
		nextPage = re.findall(r'<span class="next"><a href="(.*?)">', data, re.S)
		while nextPage:
			print "One more page is found: " + nextPage[0].strip()
			page = page +100
			data = urllib.urlopen(nextPage[0].strip()).read()
			parse_segment(data, post, author)
			nextPage = re.findall(r'<span class="next"><a href="(.*?)">', data, re.S)
	except IndexError:
		print "This is the last page."
	return page
		
def parse_segment(data, post, author):
	segments = re.findall(r'(<li class="clearfix">.*?</li>)', data, re.S)
	for seg in segments:
		try:
			re.findall(r'alt="'+author+'"/>', seg, re.S)[0].strip()
			d = re.findall(r'<h4>(.*)\n', seg)[0].strip()
			date = datetime.strptime(d, "%Y-%m-%d %H:%M:%S")
			try:
				Segment.objects.get(date=date)
			except ObjectDoesNotExist:
				content = re.findall(r'<p>(.*)</p>', seg, re.S)[0].strip()
				s = Segment(post = post, date = date, content = content)
				s.save()
		except IndexError:
			pass
		