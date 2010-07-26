from eulcore.django.existdb.manager import Manager
from eulcore.django.existdb.models import XmlModel
from eulcore.xmlmap import XmlObject
from eulcore.xmlmap.fields import StringField
from eulcore.xmlmap.teimap import Tei, TeiDiv

# TEI poetry models
# currently just slightly-modified versions of tei xmlmap objects

class PoetryBook(XmlModel, Tei):
    objects = Manager('/TEI.2')

class Poem(XmlModel, TeiDiv):
    poet = StringField("docAuthor/@n")
    objects = Manager('//div')      # should this have [@type='poem'] ?

class Poet(XmlModel, XmlObject):
    first_letter = StringField("substring(@n,1,1)")
    name  = StringField("@n")
    objects = Manager("//div[@type='poem']/docAuthor")
    
