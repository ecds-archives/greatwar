from django.http import HttpResponse, Http404
from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.cache import cache_page

from eulcore.django.fedora.server import Repository
from eulcore.fedora.util import RequestFailed

from greatwar.postcards.models import ImageObject, PostcardCollection, RepoCategories
from greatwar.postcards.forms import SearchForm

import logging

# FIXME: set repo default type somewhere in a single place

@cache_page(900)
def summary(request):
    '''Postcard summary/about page with information about the postcards and
    various entry points for accessing them.'''

    # get a list of all the postcards by searching in fedora
    # - used to get total count, and to display a random postcard
    # NOTE: this may be inefficient when all postcards are loaded; consider caching
    repo = Repository()
    search_opts = {'pid__contains': '%s:*' % settings.FEDORA_PIDSPACE }
    postcards = list(repo.find_objects(**search_opts))
    count = len(postcards)
    # TODO: get categories from fedora collection object
    categories = PostcardCollection.get().interp.content.interp_groups
    return render_to_response('postcards/index.html', {
                               'categories' : categories,
                               'count' : count,
                               'postcards': postcards,
                               },
                              context_instance=RequestContext(request))

def browse(request):
    "Browse postcards and display thumbnail images."
    repo = Repository()
    repo.default_object_type = ImageObject
    # TEMPORARY: restrict to postcards by pidspace
    # NOTE: tests rely somewhat on restriction by pidspace...
    search_opts = {'pid__contains': '%s:*' % settings.FEDORA_PIDSPACE }
    number_of_results = 15
    context = {}

    if 'subject' in request.GET:
        context['subject'] = request.GET['subject']
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
    
    return render_to_response('postcards/browse.html', context,
                                context_instance=RequestContext(request))

def view_postcard(request, pid):
    '''View a single postcard at actual postcard size, with description.'''
    repo = Repository()
    try:
        obj = repo.get_object(pid, type=ImageObject)
        obj.label   # access object label to trigger 404 before we get to the template
        return render_to_response('postcards/view_postcard.html',
                              {'card' : obj },
                                context_instance=RequestContext(request))                                                       
    except RequestFailed:
        raise Http404

# TODO: clean up image disseminations, make more efficient
def postcard_image(request, pid, size):
    '''Serve out postcard image in requested size.

    :param pid: postcard object pid
    :param size: size to return, one of thumbnail, medium, or large
    '''
    try:
        repo = Repository()
        obj = repo.get_object(pid, type=ImageObject)
        if size == 'thumbnail':
            image = obj.thumbnail()
        elif size == 'medium':
            image = obj.medium_image()
        elif size == 'large':
            image = obj.large_image()
        
        return HttpResponse(image, mimetype='image/jpeg')
    
    except RequestFailed as fail:
        raise Http404


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
