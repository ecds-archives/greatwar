from eulcore.django.existdb.manager import Manager
from eulcore.django.existdb.models import XmlModel
#from eulcore.fedora.models import DigitalObject, FileDatastream
from eulcore.xmlmap.teimap import TeiFigure, TeiInterpGroup, TeiInterp


# TEI postcard models

class Postcard(XmlModel, TeiFigure):
    # entity, head, ana, and description all inherited from TeiFigure    
    objects = Manager("//figure")


class Categories(XmlModel, TeiInterpGroup):
    objects = Manager("//interpGrp")

#class KeyValue(XmlModel, TeiInterp):
#    objects = Manager("//interp")

# preliminary fedora object for images
#class ImageObject(DigitalObject):
#    # DC & RELS-EXT inherited
#    image = FileDatastream("IMAGE", "Master TIFF image", defaults={
#            'mimetype': 'image/tiff',
            # FIXME: versioned? checksum?
#        })
