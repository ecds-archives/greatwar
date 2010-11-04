from django.conf import settings

from eulcore.django.existdb.manager import Manager
from eulcore.django.existdb.models import XmlModel
from eulcore.django.fedora import Repository
from eulcore.fedora.models import DigitalObject, FileDatastream, XmlDatastream
from eulcore.xmlmap import XmlObject
from eulcore.xmlmap.fields import NodeListField
from eulcore.xmlmap.teimap import TeiFigure, TeiInterpGroup, TeiInterp, TeiLineGroup
from eulcore.xmlmap.teimap import TEI_NAMESPACE

# TEI postcard models

class Postcard(XmlModel, TeiFigure):
    # entity, head, ana, and description all inherited from TeiFigure    
    objects = Manager("//figure")
    interp_groups = NodeListField('ancestor::text//interpGrp', TeiInterpGroup)
    
    interps = NodeListField('ancestor::text//interp[contains(string($n/@ana), @id)]', TeiInterp)
    #interp_xquery='''for $i in collection("/db/greatwar")//interp
    #            where contains($n/@ana, $i/@id)
    #            return <interp>{$i/@*}{$i/parent::node()/@type}</interp>'''


class Categories(XmlModel, TeiInterpGroup):
    objects = Manager("//interpGrp")

class KeyValue(XmlModel, TeiInterp):
    objects = Manager("//interp")

# preliminary fedora object for images
class ImageObject(DigitalObject):
    CONTENT_MODELS = [ 'info:fedora/djatoka:jp2CModel' ]
    
    # DC & RELS-EXT inherited
    # NOTE: dsid 'source' required for djatoka cmodel image service
    image = FileDatastream("source", "Master TIFF image", defaults={
            'mimetype': 'image/tiff',
            # FIXME: versioned? checksum?
        })

    def thumbnail(self):
        # shortcut to image dissemination
        return self.getDissemination('djatoka:jp2SDef', 'getRegion', {'level': '1'})


# map interpgroup into a categories object that can be used as fedora datastream class
class RepoCategories(XmlObject):
    interp_groups = NodeListField("interpGrp", TeiInterpGroup)

class PostcardCollection(DigitalObject):
    CONTENT_MODELS = [ 'info:fedora/emory-control:Collection-1.0' ]

    interp = XmlDatastream("INTERP", "Postcard Categories", RepoCategories, defaults={
            'mimetype': 'application/xml',
            'versionable': True,
        })

    @staticmethod
    def get():
        # retrive configured postcard collection object
        repo = Repository()
        return repo.get_object(settings.POSTCARD_COLLECTION_PID, type=PostcardCollection)
