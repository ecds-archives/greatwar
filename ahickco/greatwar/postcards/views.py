from greatwar.postcards.models import PostcardThumb
from django.http import HttpResponse
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from eulcore.django.existdb.db import ExistDB
from eulcore.existdb.exceptions import DoesNotExist

def postcards(request):
    "Browse thumbnail list of postcards"
    postcards = PostcardThumb.objects.only('head', 'entity')
    return render_to_response('postcards/postcards.html', { 'postcards' : postcards,
                                                         })

    
