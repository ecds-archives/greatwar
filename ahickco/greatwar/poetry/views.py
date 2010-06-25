from django.shortcuts import render_to_response
from greatwar.poetry.models import PoetryBook, Poem, Poet
from django.http import HttpResponse
from django.core.paginator import Paginator, InvalidPage, EmptyPage


def books(request):
    "Browse list of volumes"
    books = PoetryBook.objects.only(['id', 'title', 'author', 'editor'])
    return render_to_response('poetry/books.html', { 'books' : books,
                                                     'querytime' : books.queryTime()})


def book_toc(request, doc_id):
    "Display the contents of a book"
    #book = PoetryBook.objects.getDocument(docname)
    book = PoetryBook.objects.get(id__exact=doc_id)
    return render_to_response('poetry/book_toc.html', { 'book' : book})

def div(request, doc_id, div_id):
    "Display a single div (poem)"
    div = Poem.objects.also(['doctitle', 'doc_id']).filter(doc_id__exact=doc_id).get(id__exact=div_id)
    body = div.xslTransform(filename='templates/xslt/div.xsl')
    return render_to_response('poetry/div.html', { 'div' : div,
                                                   'body' : body})   
def poets(request):
    "Browse list of poets"
    return _show_poets(request, Poet.objects.only(['name']).distinct().order_by('name'))

def poets_by_firstletter(request, letter):
    "Browse list of poets by first letter"
    return _show_poets(request, Poet.objects.filter(name__startswith=letter).only(['name']).distinct().order_by('name'), letter)


def _show_poets(request, poets, current_letter=None):
    poet_paginator = Paginator(poets, 50)
    first_letters = Poet.objects.only(['first_letter']).order_by('name').distinct()
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
    poems = Poem.objects.filter(poet__exact=name).also(['doctitle', 'doc_id']).order_by('title').all()
    return render_to_response('poetry/poem_list.html', { 'poems' : poems,
                                                         'poet'  : name,
                                                         'querytime' : poems.queryTime()})
