from eulcore.django.existdb.manager import Manager
from eulcore.django.existdb.models import XmlModel
#from eulcore.fedora.models import DigitalObject, FileDatastream
from eulcore.xmlmap.teimap import TeiFigure, TeiInterpGroup


# TEI postcard models

class Postcard(XmlModel, TeiFigure):
    # entity, head, ana, and description all inherited from TeiFigure    
    objects = Manager("//figure")

    def ana_split(self, value):
        if isinstance(value, ana):
            ana_list = string.split(ana)
            return ana_list

class Card(XmlModel, TeiFigure):
    objects = Manager("//figure[@entity]")

class Categories(XmlModel, TeiInterpGroup):
    objects = Manager("//interpGrp")

# preliminary fedora object for images
#class ImageObject(DigitalObject):
#    # DC & RELS-EXT inherited
#    image = FileDatastream("IMAGE", "Master TIFF image", defaults={
#            'mimetype': 'image/tiff',
            # FIXME: versioned? checksum?
#        })
