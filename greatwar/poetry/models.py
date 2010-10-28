from eulcore.django.existdb.manager import Manager
from eulcore.django.existdb.models import XmlModel
from eulcore.xmlmap import XmlObject
from eulcore.xmlmap.fields import StringField, NodeField, StringListField, NodeListField
from eulcore.xmlmap.teimap import Tei, TeiDiv, TeiLineGroup, TEI_NAMESPACE

# TEI poetry models
# currently just slightly-modified versions of tei xmlmap objects



class PoetryBook(XmlModel, Tei):
    ROOT_NAMESPACES = {'tei' : TEI_NAMESPACE}
    objects = Manager('/tei:TEI')

class Poem(XmlModel, TeiDiv):
    ROOT_NAMESPACES = {'tei' : TEI_NAMESPACE}
    poet = StringField("tei:docAuthor/tei:name/tei:choice")
    poetrev = StringField("tei:docAuthor/tei:name/tei:choice/tei:reg")
    nextdiv = NodeField("following::tei:div[@type='poem'][1]", "self")
    prevdiv = NodeField("preceding::tei:div[@type='poem'][1]", "self")
    poem = NodeField("tei:div[@type='poem']", "self")
    line_matches = StringListField('tei:l')   # place-holder: must be retrieved with raw xpath to use ft:query
    objects = Manager("//tei:div")      # should this have [@type='poem'] ? No, then essays are not retrieved, e.g. "Swan Song" in Eaton.

class Poet(XmlModel, XmlObject):
    ROOT_NAMESPACES = {'tei' : TEI_NAMESPACE}
    first_letter = StringField("substring(tei:reg,1,1)")
    name  = StringField("tei:reg")
    objects = Manager("//tei:div[@type='poem']/tei:docAuthor/tei:name/tei:choice")
    
