from eulcore.django.existdb.manager import Manager
from eulcore.django.existdb.models import XmlModel
from eulcore.fedora.models import DigitalObject, FileDatastream
from eulcore.xmlmap.fields import NodeListField
from eulcore.xmlmap.teimap import TeiFigure, TeiInterpGroup, TeiInterp


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
