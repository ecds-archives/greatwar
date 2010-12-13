from django.shortcuts import render_to_response

def index(request):
    "Front page"
    return render_to_response('index.html')


def about(request):
    "About the site"
    return render_to_response('about.html')

def links(request):
    "Links to sites about World War I"
    return render_to_response('links.html')
