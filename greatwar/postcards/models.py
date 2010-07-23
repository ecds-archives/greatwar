#from django.db import models
from django.conf import settings
from eulcore import xmlmap
from eulcore.xmlmap.teimap import TeiFigure
from eulcore.existdb.query import QuerySet
from eulcore.django.existdb.db import ExistDB
from eulcore.django.existdb.manager import Manager
from eulcore.xmlmap.core import XmlObject #, XPathString
from eulcore.django.existdb.models import XmlModel


# TEI postcard model
#class Postcard(TeiFigure):
#     objects = QuerySet(model=TeiFigure, xpath="/TEI.2", using=ExistDB()
#                        collection=settings.EXISTDB_ROOT_COLLECTION)

class Postcard(XmlModel, TeiFigure):
     head = xmlmap.StringField("head")
     entity = xmlmap.StringField("@entity")
     ana = xmlmap.StringField("@ana")
     description = xmlmap.StringField("figDesc")
     objects = Manager("//figure")

     def to_python(self, value):
          if isinstance(value, ana):
               ana_list = string.split(ana)
               return ana_list
Postcard.objects.model = Postcard


