import logging
from lxml import etree
from urllib import urlencode

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template import RequestContext

from eulcore.django.existdb.db import ExistDB
from eulcore.existdb.exceptions import DoesNotExist # ReturnedMultiple needed also ?
from eulcore.xmlmap.teimap import TEI_NAMESPACE

from greatwar.poetry.models import PoetryBook, Poem, Poet
from greatwar.poetry.forms import PoetrySearchForm


def books(request):
    "Browse list of volumes"
    books = PoetryBook.objects.only('id', 'title', 'author', 'editor').order_by('author')
    return render_to_response('poetry/books.html', { 'books' : books,
                                                     'querytime' : books.queryTime()})


def book_toc(request, doc_id):
    "Display the contents of a book"
    #book = PoetryBook.objects.getDocument(docname)
    book = PoetryBook.objects.get(id__exact=doc_id)
    return render_to_response('poetry/book_toc.html', { 'book' : book})

def div(request, doc_id, div_id):
    "Display a single div (poem)"
    div = Poem.objects.also('doctitle', 'doc_id', 'nextdiv__id', 'nextdiv__title', 'prevdiv__id', 'prevdiv__title').filter(doc_id__exact=doc_id).get(id__exact=div_id)
    body = div.xsl_transform(filename='poetry/xslt/div.xsl')
    print body.serialize()
    return render_to_response('poetry/div.html', { 'div' : div,
                                                   'body' : body.serialize()
                                                   })   
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
                                                     'querytime' : [poets.object_list.queryTime(),first_letters.queryTime()]
                                                     })    
    
    
def poet_list(request, name):
    "List poems by a particular poet"
    poems = Poem.objects.filter(poetrev__exact=name).also('doctitle', 'doc_id').order_by('title').all()
    return render_to_response('poetry/poem_list.html', { 'poems' : poems,
                                                         'poet'  : name,
                                                         'querytime' : poems.queryTime()})
                                                         
def search(request):
    "Search poetry by title/author/keyword"
    form = PoetrySearchForm(request.GET)
    response_code = None
    search_opts = {}
    poetry = None
    if form.is_valid(): 
        if 'title' in form.cleaned_data and form.cleaned_data['title']:
            search_opts['title__fulltext_terms'] = '%s' % form.cleaned_data['title']
        if 'author' in form.cleaned_data and form.cleaned_data['author']:
            search_opts['author__fulltext_terms'] = '%s' % form.cleaned_data['author']
        if 'keyword' in form.cleaned_data and form.cleaned_data['keyword']:
            search_opts['fulltext_terms'] = '%s' % form.cleaned_data['keyword']
                    
        poetry = Poem.objects.also("doctitle","doc_id").filter(type__exact="poem").filter(**search_opts)

    # select non-empty form values for use in template
   # search_params = dict((key, value) for key, value in form.cleaned_data.iteritems()
   #                                              if value) 

    response = render_to_response('poetry/search.html', {
                "search": form,
                "poetry": poetry,
 #               'search_params': search_params,
 #               'url_params': '?' + urlencode('search_params'),
        },
                context_instance=RequestContext(request))
    if response_code is not None:
        response.status_code = response_code
    return response                                                         
