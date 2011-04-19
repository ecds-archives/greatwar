from django.conf import settings
from django.core.management.base import CommandError
from eulcore.django.existdb.manager import Manager
from eulcore.django.existdb.models import XmlModel
from eulcore.django.fedora import Repository
from eulcore.fedora.models import DigitalObject, FileDatastream, XmlDatastream
from eulcore.xmlmap import XmlObject
from eulcore.xmlmap.fields import NodeListField
from eulcore.xmlmap.teimap import TeiFigure, TeiInterpGroup, TeiInterp, TeiLineGroup
from eulcore.xmlmap.teimap import _TeiBase
from pidservices.djangowrapper.shortcuts import DjangoPidmanRestClient
from util import get_pid_target

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
    CONTENT_MODELS = [ 'info:fedora/emory-control:Image-1.0' ]
    IMAGE_SERVICE = 'emory-control:DjatokaImageService'
    
    # DC & RELS-EXT inherited
    image = FileDatastream("source-image", "Master TIFF image", defaults={
            'mimetype': 'image/tiff',
            # FIXME: versioned? checksum?
        })
        
    default_pidspace = getattr(settings, 'FEDORA_PIDSPACE', None)

    def thumbnail(self):
        'Shortcut to thumbnail-size image dissemination.'
        return self.getDissemination(self.IMAGE_SERVICE, 'getRegion', {'level': '1'})

    def medium_image(self):
        'Shortcut to medium-size image dissemination.'
        return self.getDissemination(self.IMAGE_SERVICE, 'getRegion', {'level': '3'})

    def large_image(self):
        'Shortcut to large-size image dissemination.'
        return self.getDissemination(self.IMAGE_SERVICE, 'getRegion', {'level': '5'})

    #THIS METHOD WILL NOT WORK UNTIL get_object FUNCTION IS FIXED IN EULCORE
    def get_default_pid(self):
        # try to configure a pidman client to get pids.
        try:
            pidman = DjangoPidmanRestClient()
        except:
            raise CommandError("PIDMAN Not Configured. Plese check localsetting.py")

        target = get_pid_target('postcards:card')
        ark = pidman.create_ark(settings.PIDMAN_DOMAIN, target, self.label)
        arkbase, slash, noid = ark.rpartition('/')
        pid = '%s:%s' % (self.default_pidspace, noid)
        self.dc.content.identifier_list.append(ark) # Store local identifiers in DC
        return pid
        

# map interpgroup into a categories object that can be used as fedora datastream class
class RepoCategories(_TeiBase):
    interp_groups = NodeListField("tei:interpGrp", TeiInterpGroup)

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
