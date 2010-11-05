from django.http import HttpResponse, Http404
from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response
from django.template import RequestContext

from eulcore.django.fedora.server import Repository
from greatwar.postcards.models import ImageObject
from greatwar.postcards.forms import SearchForm

import logging

# FIXME: set repo default type somewhere in a single place

def summary(request):
   "Show the postcard home page"
   count = 0        # TODO: get count from fedora
   # TODO: get categories from fedora collection object
   return render_to_response('postcards/index.html', {
                               #'categories' : categories,
                               'count' : count,
                               },
                              context_instance=RequestContext(request))

def browse(request):
    "Browse postcards and display thumbnail images."
    repo = Repository()
    repo.default_object_type = ImageObject
    # TEMPORARY: restrict to postcards by pidspace
    search_opts = {'pid__contains': '%s:*' % settings.FEDORA_PIDSPACE }
    number_of_results = 15
    context = {}

    if 'subject' in request.GET:
        search_opts['subject'] = request.GET['subject']

    postcards = repo.find_objects(**search_opts)
    
    postcard_paginator = Paginator(list(postcards), number_of_results)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    # If page request (9999) is out of range, deliver last page of results.
    try:
        postcard_page = postcard_paginator.page(page)
    except (EmptyPage, InvalidPage):
        postcard_page = postcard_paginator.page(paginator.num_pages)
                
    context['postcards_paginated'] = postcard_page
    
    return render_to_response('postcards/browse.html',
                              context,
                                context_instance=RequestContext(request))

def view_postcard(request, pid):
    '''View a single postcard at actual postcard size, with description.'''
    repo = Repository()
    obj = repo.get_object(pid, type=ImageObject)
    # TODO: 404 if not found
    return render_to_response('postcards/view_postcard.html',
                              {'card' : obj },
                                context_instance=RequestContext(request))                                                       

# TODO: clean up image disseminations, make more efficient
# OR: can we just link to fedora image disseminations?
def thumbnail_image(request, pid):
    # serve out thumbnail image
    repo = Repository()
    obj = repo.get_object(pid, type=ImageObject)
    return HttpResponse(obj.thumbnail(), mimetype='image/jpeg')

def medium_image(request, pid):
    # serve out medium image dissemination
    repo = Repository()
    obj = repo.get_object(pid, type=ImageObject)
    return HttpResponse(obj.getDissemination('djatoka:jp2SDef', 'getRegion', {'level': '3'}),
            mimetype='image/jpeg')

def large_image(request, pid):
    # serve out large image dissemination
    repo = Repository()
    obj = repo.get_object(pid, type=ImageObject)
    return HttpResponse(obj.getDissemination('djatoka:jp2SDef', 'getRegion', {'level': '5'}),
            mimetype='image/jpeg')


def search(request):
    # rough fedora-based postcard search (borrowed heavily from digital masters)
    form = SearchForm(request.GET)
    response_code = None
    context = {'search': form}
    number_of_results = 5
    if form.is_valid(): 
        # adding wildcards because fedora has a weird notion of what 'contains' means

        # TODO: terms search can't be used with with field search
        # -- how to allow a keyword search but restrict to postcards?
        #keywords = '%s*' % form.cleaned_data['keyword'].rstrip('*')
        
        # TEMPORARY: restrict to postcards by pidspace
        search_opts = {'pid__contains': '%s:*' % settings.FEDORA_PIDSPACE }
        if 'title' in form.cleaned_data:
            search_opts['title__contains'] = '%s*' % form.cleaned_data['title'].rstrip('*')
        if 'description' in form.cleaned_data:
            search_opts['description__contains'] = '%s*' % form.cleaned_data['description'].rstrip('*')
        try:
            repo = Repository()          
            found = repo.find_objects(type=ImageObject, **search_opts)
            
            search_paginator = Paginator(list(found), number_of_results)
            try:
                page = int(request.GET.get('page', '1'))
            except ValueError:
                page = 1
            # If page request (9999) is out of range, deliver last page of results.
            try:
                search_page = search_paginator.page(page)
            except (EmptyPage, InvalidPage):
                search_page = search_paginator.page(paginator.num_pages)
                
            
            context['postcards_paginated'] = search_page   
            context['title'] = form.cleaned_data['title']
            context['description'] = form.cleaned_data['description']
        except Exception as e:
            logging.debug(e)
            response_code = 500
            context['server_error'] = 'There was an error ' + \
                    'contacting the digital repository. This ' + \
                    'prevented us from completing your search. If ' + \
                    'this problem persists, please alert the ' + \
                    'repository administrator.'

    response = render_to_response('postcards/search.html', context,
                context_instance=RequestContext(request))
    if response_code is not None:
        response.status_code = response_code
    return response





 # object pagination - adapted directly from django paginator documentation
 # from findingaids/fa/util.py to here
def paginate_queryset(request, qs, per_page=10, orphans=0):    # 0 is django default
    # FIXME: should num-per-page be configurable via local settings?
    paginator = Paginator(qs, per_page, orphans=orphans)
    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    # If page request (9999) is out of range, deliver last page of results.
    try:
        paginated_qs = paginator.page(page)
    except InvalidPage:
        raise http.Http404
    except EmptyPage:       # ??
        paginated_qs = paginator.page(paginator.num_pages)

    return paginated_qs, paginator
   

def pages_to_show(paginator, page):
    # generate a list of pages to show around the current page
    # show 3 numbers on either side of current number, or more if close to end/beginning
    show_pages = []
    if page != 1:
        before = 3      # default number of pages to show before the current page
        if page >= (paginator.num_pages - 3):   # current page is within 3 of end
            # increase number to show before current page based on distance to end
            before += (3 - (paginator.num_pages - page))
        for i in range(before, 0, -1):    # add pages from before away up to current page
            if (page - i) >= 1:
                show_pages.append(page - i)
    # show up to 3 to 7 numbers after the current number, depending on how many we already have
    for i in range(7 - len(show_pages)):
        if (page + i) <= paginator.num_pages:
            show_pages.append(page + i)

    return show_pages
