from greatwar.postcards.models import Postcard
from django.http import HttpResponse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response
from eulcore.django.existdb.db import ExistDB
from eulcore.existdb.exceptions import DoesNotExist

def postcards(request):
    "Browse thumbnail list of postcards"
    postcards = Postcard.objects.only('head', 'entity')
    count = Postcard.objects.count()
    paginator = paginate_queryset(request, postcards) #show 50 thumbnails per page
    postcard_subset, paginator = paginate_queryset(request, postcards, per_page=50, orphans=3)
    show_pages = pages_to_show(paginator, postcard_subset.number)
    return render_to_response('postcards/postcards.html', { 'postcards' : postcard_subset, 
                                                         'show_pages' : show_pages,
                                                          'count' : count, })

def card(request):
    "Show an individual card at real size with description"
    card = Postcard.objects.only('head', 'entity', 'ana', 'figDesc')
    return render_to_resonse('postcards/card.html', { 'card' : card, })

def index():
   "Show the postcard home page"
   return render_to_response('postcards/index.html', { 'index' : index, })


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
