from django.conf import settings
from eulcore.xmlmap.teimap import Tei, TeiDiv
from eulcore.existdb.query import QuerySet
from eulcore.django.existdb.db import ExistDB
from eulcore.xmlmap.core import XmlObject, XPathString


# TEI poetry model
# currently just a wrapper around tei xmlmap object,
# with a exist queryset initialized using django-exist settings and tei model

class PoetryBook(Tei):
    objects = QuerySet(model=Tei, xpath="/TEI.2", using=ExistDB(),
                       collection=settings.EXISTDB_ROOT_COLLECTION)

    poems  = XPathString('text/body//div[@type="poem"]')

class Poem(TeiDiv):
    objects = QuerySet(model=TeiDiv, xpath="//div", using=ExistDB(),
                       collection=settings.EXISTDB_ROOT_COLLECTION)

class Poet(XmlObject):
    xpath = "//div[@type='poem']/docAuthor/@n"
    objects = QuerySet(model=TeiDiv, xpath="//div", using=ExistDB(),
                       collection=settings.EXISTDB_ROOT_COLLECTION)

    
    
