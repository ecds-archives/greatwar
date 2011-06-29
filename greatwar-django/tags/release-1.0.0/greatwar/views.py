from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request):
    "Front page"
    return render_to_response('index.html', {}, context_instance=RequestContext(request))


def about(request):
    "About the site"
    return render_to_response('about.html', {}, context_instance=RequestContext(request))

def links(request):
    "Links to sites about World War I"
    return render_to_response('links.html', {}, context_instance=RequestContext(request))

def credits(request):
    "Site production credits"
    return render_to_response('credits.html', {}, context_instance=RequestContext(request))
