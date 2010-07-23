from django.conf import settings
from eulcore import xmlmap
from eulcore.xmlmap.teimap import Tei, TeiDiv
from eulcore.existdb.query import QuerySet
from eulcore.django.existdb.db import ExistDB
from eulcore.xmlmap.core import XmlObject #, XPathString
from eulcore.django.existdb.models import XmlModel

# TEI poetry model
# currently just a wrapper around tei xmlmap object,
# with a exist queryset initialized using django-exist settings and tei model

class PoetryBook(Tei):
    objects = QuerySet(model=Tei, xpath="/TEI.2", using=ExistDB(),
                       collection=settings.EXISTDB_ROOT_COLLECTION)

class Poem(TeiDiv):
    poet = xmlmap.StringField("docAuthor/@n")
    objects = QuerySet(model=TeiDiv, xpath="//div", using=ExistDB(),
                       collection=settings.EXISTDB_ROOT_COLLECTION)
Poem.objects.model = Poem

class Poet(XmlObject):
    first_letter = xmlmap.StringField("substring(@n,1,1)")
    name  = xmlmap.StringField("@n")
    objects = QuerySet(xpath="//div[@type='poem']/docAuthor",
                       using=ExistDB(),
                       collection=settings.EXISTDB_ROOT_COLLECTION)
Poet.objects.model = Poet

    
