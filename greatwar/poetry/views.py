import os
from urllib import urlencode

from django.conf import settings
from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template import RequestContext

from eulcommon.djangoextras.http import content_negotiation
from eulexistdb.query import escape_string
from eulexistdb.exceptions import DoesNotExist # ReturnedMultiple needed also ?

from greatwar.poetry.models import PoetryBook, Poem, Poet, PoemSearch
from greatwar.poetry.forms import PoetrySearchForm


def books(request):
    "Browse list of volumes"
    books = PoetryBook.objects.only('id', 'title', 'author', 'editor').order_by('author')
    return render_to_response('poetry/books.html', {'books' : books}, context_instance=RequestContext(request))

def book_xml(request, doc_id):
    "Display the original TEI XML for a single book."
    try:
        book = PoetryBook.objects.get(id__exact=doc_id)
        xml_tei = book.serialize(pretty=True)
        return HttpResponse(xml_tei, content_type='application/tei+xml')
    except DoesNotExist:
        raise Http404

@content_negotiation({'application/tei+xml': book_xml})
def book_toc(request, doc_id):
    "Display the contents of a single book."
    try:
        book = PoetryBook.objects.get(id__exact=doc_id)
        return render_to_response('poetry/book_toc.html', {'book': book}, context_instance=RequestContext(request))
    except DoesNotExist:
        raise Http404

def div(request, doc_id, div_id):
    "Display a single div (poem or essay)"
    if 'keyword' in request.GET:
        search_terms = request.GET['keyword']
        url_params = '?' + urlencode({'keyword': search_terms})
        filter = {'highlight': search_terms}
    else:
        url_params = ''
        filter = {}
    try:
        extra_fields = ['book__id', 'book__title', 'nextdiv__id', 'nextdiv__title',
            'prevdiv__id', 'prevdiv__title', 'book__source']
        div = Poem.objects.also(*extra_fields).filter(book__id=doc_id, **filter).get(id=div_id)
        body = div.xsl_transform(filename=os.path.join(settings.BASE_DIR, 'poetry', 'xslt', 'div.xsl'))
        return render_to_response('poetry/div.html', { 'div' : div,
                                                       'body' : body.serialize(),
                                                       'url_params' : url_params,
                                                       }, context_instance=RequestContext(request))
    except DoesNotExist:
        raise Http404


def poets(request):
    "Browse list of poets"
    return _show_poets(request, Poet.objects.only('name').distinct().order_by('name'))

def poets_by_firstletter(request, letter):
    "Browse list of poets by first letter"
    return _show_poets(request, Poet.objects.filter(name__startswith=letter).only('name').distinct().order_by('name'), letter)


def _show_poets(request, poets, current_letter=None):
    poet_paginator = Paginator(poets, 50)
    first_letters = Poet.objects.only('first_letter').order_by('name').distinct()
    # pagination options (from django docs)
    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    # If page request (9999) is out of range, deliver last page of results.
    try:
        poets = poet_paginator.page(page)
    except (EmptyPage, InvalidPage):
        poets = poet_paginator.page(paginator.num_pages)

    return render_to_response('poetry/poets.html', { 'poets' : poets,
                                                     'first_letters' : first_letters,
                                                     'current_letter' : current_letter,
                                                     }, context_instance=RequestContext(request))


def poet_list(request, name):
    "List poems by a particular poet"
    poems = Poem.objects.filter(poetrev__exact=name).also('book__title',
                        'book__id').order_by('title').all()
    return render_to_response('poetry/poem_list.html', { 'poems' : poems,
                                                         'poet'  : name,
                                                         }, context_instance=RequestContext(request))

def search(request):
    "Search poetry by title/author/keyword"
    form = PoetrySearchForm(request.GET)
    response_code = None
    search_opts = {}
    poetry = None
    number_of_results = 10


    if form.is_valid():
        if 'title' in form.cleaned_data and form.cleaned_data['title']:
            search_opts['title_list__fulltext_terms'] = '%s' % form.cleaned_data['title']
        if 'author' in form.cleaned_data and form.cleaned_data['author']:
            search_opts['docauthor__fulltext_terms'] = '%s' % form.cleaned_data['author']
        if 'keyword' in form.cleaned_data and form.cleaned_data['keyword']:
            search_opts['fulltext_terms'] = '%s' % form.cleaned_data['keyword']

        poems = PoemSearch.objects.only("book__title","book__id","title", "id").filter(**search_opts)
        if 'keyword' in form.cleaned_data and form.cleaned_data['keyword']:
            poems = poems.only_raw(line_matches='%%(xq_var)s//tei:l[ft:query(., "%s")]' \
                                    % escape_string(form.cleaned_data['keyword']))
        poetry = poems.all()
        search_paginator = Paginator(poetry, number_of_results)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        # If page request (9999) is out of range, deliver last page of results.
        try:
            search_page = search_paginator.page(page)
        except (EmptyPage, InvalidPage):
            search_page = search_paginator.page(paginator.num_pages)

        response = render_to_response('poetry/search.html', {
                "search": form,
                "poetry_paginated": search_page,
                "keyword": form.cleaned_data['keyword'],
                "title": form.cleaned_data['title'],
                "author": form.cleaned_data['author'],
        },
        context_instance=RequestContext(request))
    #no search conducted yet, default form
    else:
        response = render_to_response('poetry/search.html', {
                    "search": form
            },
            context_instance=RequestContext(request))

    if response_code is not None:
        response.status_code = response_code
    return response
