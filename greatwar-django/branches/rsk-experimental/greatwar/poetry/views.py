from django.shortcuts import render_to_response
from greatwar.poetry.models import PoetryBook, Poem
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
    body = div.xslTransform(filename='templates/poetry/div.xsl')
    return render_to_response('poetry/div.html', { 'div' : div,
                                                   'body' : body})
   
    

