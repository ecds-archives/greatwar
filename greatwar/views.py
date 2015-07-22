from django.shortcuts import render

def index(request):
    "Front page"
    return render(request, 'index.html')


def about(request):
    "About the site"
    return render(request ,'about.html')

def links(request):
    "Links to sites about World War I"
    return render(request, 'links.html')

def credits(request):
    "Site production credits"
    return render(request, 'credits.html')
