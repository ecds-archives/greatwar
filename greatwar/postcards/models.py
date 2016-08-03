import logging
from django.conf import settings
from django.core.management.base import CommandError

from eulxml.xmlmap.fields import NodeListField, StringField
from eulxml.xmlmap import teimap
from eulexistdb.manager import Manager
from eulexistdb.models import XmlModel

from eulfedora.server import Repository
from eulfedora.models import DigitalObject, FileDatastream, XmlDatastream
from pidservices.djangowrapper.shortcuts import DjangoPidmanRestClient
from piffle.iiif import IIIFImageClient

from util import get_pid_target


logger = logging.getLogger(__name__)


# TEI postcard models

# NOTE: extending eulxml.teimap to find interp value in value attribute;
# this was used previously, but for correct TEI it should be the text
# content within the interp element; supporting both here so that the
# postcard interp data need not be changed.

class TeiInterp(teimap.TeiInterp):
    value = StringField('text()|@value')


class TeiInterpGroup(teimap.TeiInterpGroup):
    interp = NodeListField("tei:interp", TeiInterp)


class Postcard(XmlModel, teimap.TeiFigure):
    # entity, head, ana, and description all inherited from TeiFigure
    objects = Manager("//figure")
    interp_groups = NodeListField('ancestor::text//interpGrp', TeiInterpGroup)

    interps = NodeListField('ancestor::text//interp[contains(string($n/@ana), @id)]', TeiInterp)
    #interp_xquery='''for $i in collection("/db/greatwar")//interp
    #            where contains($n/@ana, $i/@id)
    #            return <interp>{$i/@*}{$i/parent::node()/@type}</interp>'''


class Categories(XmlModel, teimap.TeiInterpGroup):
    objects = Manager("//interpGrp")


class KeyValue(XmlModel, TeiInterp):
    objects = Manager("//interp")


# preliminary fedora object for images
class ImageObject(DigitalObject):
    CONTENT_MODELS = ['info:fedora/emory-control:Image-1.0']
    IMAGE_SERVICE = 'emory-control:DjatokaImageService'

    # DC & RELS-EXT inherited
    image = FileDatastream("source-image", "Master TIFF image", defaults={
            'mimetype': 'image/tiff',
            # FIXME: versioned? checksum?
        })

    default_pidspace = getattr(settings, 'FEDORA_PIDSPACE', None)

    @property
    def iiif_image(self):
        img_id = '%s%s' % (getattr(settings, 'IIIF_ID_PREFIX', ''),
                           self.pid)
        return IIIFImageClient(settings.IIIF_API_ENDPOINT, img_id)

    @property
    def thumbnail_url(self):
        return self.iiif_image.size(width=122, height=122, exact=True).format('png')

    @property
    def medium_img_url(self):
        return self.iiif_image.size(width=400, height=400, exact=True).format('png')

    @property
    def large_img_url(self):
        return self.iiif_image.size(width=800, height=800, exact=True).format('png')

    def get_default_pid(self):
        # try to configure a pidman client to get pids.
        try:
            pidman = DjangoPidmanRestClient()
        except:
            if getattr(settings, 'DEV_ENV', False):
                logger.warn('Failed to configure PID manager client; default pid logic will be used')
                pidman = None
            else:
                raise CommandError("PID manager is not configured. Please check localsetting.py")

        if pidman:
            target = get_pid_target('postcards:card')
            ark = pidman.create_ark(settings.PIDMAN_DOMAIN, target, self.label)
            arkbase, slash, noid = ark.rpartition('/')
            pid = '%s:%s' % (self.default_pidspace, noid)
            # Store local identifiers in DC
            self.dc.content.identifier_list.append(ark)
            return pid

        else:
            # if pidmanager is not available, fall back to default pid behavior
            return super(ImageObject, self).get_default_pid()


# map interpgroup into a categories object that can be used as fedora datastream class
class RepoCategories(teimap._TeiBase):
    interp_groups = NodeListField("tei:interpGrp", TeiInterpGroup)


class PostcardCollection(DigitalObject):
    CONTENT_MODELS = ['info:fedora/emory-control:Collection-1.0']

    interp = XmlDatastream("INTERP", "Postcard Categories", RepoCategories, defaults={
            'mimetype': 'application/xml',
            'versionable': True,
        })

    @staticmethod
    def get():
        # retrive configured postcard collection object
        repo = Repository()
        return repo.get_object(settings.POSTCARD_COLLECTION_PID, type=PostcardCollection)
