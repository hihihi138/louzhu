from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect

def main(request):
	if 'url' in request.GET:
		url = request.GET['url']
		return redirect('/'+url, permanent=True)
	else:
		return render_to_response('main_search_form.html')
	
def format_douban_url(requeset, url_tail):
	return redirect('/douban/'+url_tail, permanent=True)