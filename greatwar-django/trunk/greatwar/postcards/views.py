from django.http import HttpResponse, Http404
from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext

from eulcore.django.existdb.db import ExistDB
from eulcore.existdb.exceptions import DoesNotExist
from eulcore.django.fedora.server import Repository

from greatwar.postcards.models import Postcard, Categories, KeyValue, ImageObject, PostcardCollection
from greatwar.postcards.forms import SearchForm

def postcards(request):
    "Browse thumbnail list of postcards"
    postcards = Postcard.objects.only('head', 'entity')
    count = Postcard.objects.count()
    paginator = paginate_queryset(request, postcards) #show 50 thumbnails per page
    postcard_subset, paginator = paginate_queryset(request, postcards, per_page=50, orphans=3) #FIXME paginator doesn't show
    show_pages = pages_to_show(paginator, postcard_subset.number)
    return render_to_response('postcards/postcards.html',
                              { 'postcards' : postcard_subset, 
                                'show_pages' : show_pages,
                                'count' : count, },
                                context_instance=RequestContext(request))

def card(request, entity):
    "Show an individual card at real size with description"
    card = Postcard.objects.also('head', 'entity', 'ana', 'figDesc').filter(entity=entity).get()
    ana_list = str.split('card.ana')
    #categories = Categories.objects.also('type', 'interp'('id', 'value')) #How to render interp groups?
    #key_value = Interp.objects.only('id', 'value')
    return render_to_response('postcards/card.html',
                              { 'card' : card,
                                'ana_list' : ana_list,
                                #'categories' :  {'type': 'interp'},
                                #'interp' : {'id': 'value'}
                                                       })

def index(request):
   "Show the postcard home page"
   count = Postcard.objects.count()   
   categories = PostcardCollection.get().interp.content
   #categories = Categories.objects.also('type', 'interp') #How to render interp groups?
   return render_to_response('postcards/index.html',
                             { 'index' : index,
                               'categories' : categories,
                               'count' : count, })

def about(request):
    "Show the about page"
    about = include('about.xml')
    return render_to_response('postcards/about.html',
                              { 'about' : about,})


def searchform(request):
    "Show a detailed search form page"
    categories = Categories.objects.only('type', )
    keyvalue = KeyValue.objects.only('id', 'value')
    return render_to_response('postcards/search.html',
                              {'categories' : categories,
                               'keyvalue' : keyvalue, })
    


## EXPERIMENTAL - fedora-based views for postcards

def fedora_postcards(request):
    "EXPERIMENTAL fedora-based postcard browse"
    
    repo = Repository()
    repo.default_object_type = ImageObject
    # TEMPORARY: restrict to postcards by pidspace
    search_opts = {'pid__contains': '%s:*' % settings.FEDORA_PIDSPACE }

    if 'subject' in request.GET:
        search_opts['subject'] = request.GET['subject']

    postcards = repo.find_objects(**search_opts)
    return render_to_response('postcards/repo_postcards.html',
                              { 'postcards' : postcards },
                                context_instance=RequestContext(request))

def search(request):
    # rough fedora-based postcard search (borrowed heavily from digital masters)
    form = SearchForm(request.GET)
    response_code = None
    context = {'search': form}
    if form.is_valid() and \
        'title' in request.GET or 'description' in request.GET:
        # TODO: custom form validation -- at least one search term is required

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
            context['postcards'] = list(found)
        except:
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

def repo_thumbnail(request, pid):
    # serve out thumbnail image
    repo = Repository()
    obj = repo.get_object(pid, type=ImageObject)
    return HttpResponse(obj.thumbnail(), mimetype='image/jpeg')

def repo_medium_img(request, pid):
    # serve out medium image dissemination
    repo = Repository()
    obj = repo.get_object(pid, type=ImageObject)
    return HttpResponse(obj.getDissemination('djatoka:jp2SDef', 'getRegion', {'level': '3'}),
            mimetype='image/jpeg')

def repo_large_img(request, pid):
    # serve out large image dissemination
    repo = Repository()
    obj = repo.get_object(pid, type=ImageObject)
    return HttpResponse(obj.getDissemination('djatoka:jp2SDef', 'getRegion', {'level': '5'}),
            mimetype='image/jpeg')

def repo_postcard(request, pid):
    repo = Repository()
    obj = repo.get_object(pid, type=ImageObject)
    return render_to_response('postcards/repo_postcard.html',
                              { 'card' : obj },
                                context_instance=RequestContext(request))


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

