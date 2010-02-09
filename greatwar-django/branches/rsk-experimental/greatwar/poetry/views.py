from django.shortcuts import render_to_response
from greatwar.poetry.models import PoetryBook, Poem, Poet
from django.http import HttpResponse
from django.core.paginator import Paginator, InvalidPage, EmptyPage


def books(request):
    "Browse list of volumes"
    books = PoetryBook.objects.only(['title', 'author', 'editor'])
    return render_to_response('poetry/books.html', { 'books' : books })


def book_toc(request, docname):
    "Display the contents of a book"
    #book = PoetryBook.objects.getDocument(docname)
    book = PoetryBook.objects.get(title__exact=docname)
    return render_to_response('poetry/book_toc.html', { 'book' : book })

def div(request, docname, div_id):
    "Display a single div (poem)"
    div = Poem.objects.also(['doctitle', 'doc_id']).get(id__exact=div_id)
    body = div.xslTransform(filename='templates/xslt/div.xsl')
    return render_to_response('poetry/div.html', { 'div' : div,
                                                   'body' : body})   
def poets(request):
    "Browse list of poets"
    poet_paginator = Paginator(Poet.objects.distinct().order_by('.'), 50)
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
    
    return render_to_response('poetry/poets.html', { 'poets' : poets })
    
def poet_list(request, name):
    "List poems by a particular poet"
    poems = Poem.objects.filter(poet__exact=name).also(['doctitle', 'doc_id']).order_by('title').all()
    return render_to_response('poetry/poem_list.html', { 'poems' : poems,
                                                         'poet'  : name})
