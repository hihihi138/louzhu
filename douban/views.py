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
import threading
from helpers.threadpool import *
#from helpers.work import *

#@cache_page(60 * 5)
def post(request, slug):
	# Format the paths to /douban/slug/
	path = '/douban/'+slug+'/'
	if request.path != (path):
		return redirect(path)
	data = urllib.urlopen('http://www.douban.com/group/topic/'+slug).read()
	# Check whether the post has already existed.
	try:
		post = Post.objects.get(slug=slug)
		print "The post is already in database."
	except ObjectDoesNotExist:
		print "New post, add it now."
		add_post(slug, data)
		post = Post.objects.get(slug=slug)
	# Set the current page number.
	try:
		page = re.findall('">(\d*)</a><span class="next">', data, re.S)[0]
	except IndexError:
		page = '1'
	try:
		# Get all the segments.
		get_segment(post, page)
		# Save the page number.
		if post.page != page:
			post.page = page
			post.save()
	except:
		print "There was something wrong while parsing the segments."
	
	# Render with template.
	segments = Segment.objects.filter(post=post)
	extra_context = {'name': post.name, 'url': post.url, 'author': post.author, 'author_url': post.author_url, 'dgroup': post.dgroup, 'dgroup_url': post.dgroup_url}
	return object_list(request, template_name='post.html', queryset=segments, paginate_by=50, extra_context=extra_context)
	
def add_post(slug, data):
	try:
		name = re.findall(r'<title>(.*?)</title>', data, re.S)[0].strip()
		url = "http://www.douban.com/group/topic/"+slug+"/"
		author = re.findall(r'<span class="pl20">.*?">(.*?)</a>', data, re.S)[0].strip()
		author_url = re.findall(r'<span class="pl20">.*?href="(.*?)">', data, re.S)[0].strip()
		d = re.findall(r'<span class="color-green">(.*?)</span>', data, re.S)[0]
		post_date = datetime.strptime(d, "%Y-%m-%d %H:%M:%S")
		last_date = datetime.now()
		dgroup = re.findall(r'/">回(.*)小组</a></p><br/>', data, re.S)[0]
		dgroup_url = re.findall(r'&gt; <a href="(.*)">回', data, re.S)[0]
		p = Post(name=name,url=url,author=author,author_url=author_url,post_date=post_date,last_date=last_date,slug=slug,page=1,dgroup=dgroup,dgroup_url=dgroup_url)
		p.save()
		content = re.findall(r'<p>(.*?)</p>', data, re.S)[0].strip()
		s = Segment(post = p, date = post_date, content = content)
		s.save()
	except IndexError:
		return "There was something wrong while creating the post."

#def get_segment(post, page):
#	global database_lock 
#	database_lock = threading.Lock()
#	threads = []
#	for p in xrange(post.page, int(page)+1):
#		threads.append(threading.Thread(target=parse_segment, args=(post, p)))
#	for t in threads:
#		t.start()
#	for t in threads:
#		t.join()

def get_segment(post, page):
	global database_lock
	database_lock = threading.Lock()
	args = []
	for p in xrange(post.page, int(page)+1):
		args.append(((post,p), {}))
	requests = makeRequests(parse_segment, args)
	# Define the muti-thread number.
	pool = ThreadPool(5)
	for req in requests:
		pool.putRequest(req)
		print "Work request #%s added." % req.requestID
	pool.wait()
		
def parse_segment(post, p):
	global database_lock
	url = 'http://www.douban.com/group/topic/'+post.slug+'/?start='+str((p-1)*100)
	author = post.author.encode('UTF-8')
	data = urllib.urlopen(url).read()
	segments = re.findall(r'(<li class="clearfix">.*?</li>)', data, re.S)
	threading.currentThread().setName("processing page: "+str(p))
	print threading.currentThread().getName()
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
				database_lock.acquire()
				s.save()
				database_lock.release()
		except IndexError:
			pass
		