from django.shortcuts import render_to_response
from greatwar.poetry.models import PoetryBook, Poem, Poet
from django.http import HttpResponse


def books(request):
    books = PoetryBook.objects.only(['title', 'author', 'editor'])
    return render_to_response('poetry/books.html', { 'books' : books })


def book_toc(request, docname):  
    #book = PoetryBook.objects.getDocument(docname)
    book = PoetryBook.objects.get(title__exact=docname)
    return render_to_response('poetry/book_toc.html', { 'book' : book })

def div(request, docname, div_id):
    div = Poem.objects.also(['doctitle', 'doc_id']).get(id__exact=div_id)
    body = div.xslTransform(filename='templates/xslt/div.xsl')
    return render_to_response('poetry/div.html', { 'div' : div,
                                                   'body' : body})
   
def poet(request):
    poets = Poet.objects.distinct().order_by('.').all()
    return render_to_response('poetry/poets.html', { 'poets' : poets })
    
def poet_list(request, name):
    poems = Poem.objects.filter(poet__exact=name).also(['doctitle', 'doc_id']).order_by('title').all()
    return render_to_response('poetry/poem_list.html', { 'poems' : poems,
                                                         'poet'  : name})
