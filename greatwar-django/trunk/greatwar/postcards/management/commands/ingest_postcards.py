import os

from django.conf import settings
from django.core.management.base import BaseCommand

from eulcore.django.fedora.server import Repository

from greatwar.postcards.models import ImageObject, Postcard

 # very rough - preliminary version of ingest script
 # currently expects MASTERS_SOURCE directory configured in settings
 # - possibly should be switched to a command-line option

class Command(BaseCommand):        
    """ingest postcards...
"""
    help = __doc__

    def handle(self, *args, **options):
        verbosity = int(options['verbosity'])    # 1 = normal, 0 = minimal, 2 = all
        v_normal = 1
        v_all = 2

        repo = Repository()
        #ImageObject
        cards = Postcard.objects.all()
        for c in cards:
            file = os.path.join(settings.MASTERS_SOURCE, 'wwi_%s.tif' % c.entity)
            if os.access(file, os.F_OK):
                print "Found master file %s for %s" % (file, c.entity)
                obj = repo.get_object(type=ImageObject)
                obj.label = c.head
                obj.dc.content.title = obj.label
                obj.dc.content.description = c.description
                # TODO: convert ana attributes into meaningful DC equivalents
                obj.image.content = open(file)
                obj.save()
                print "ingested %s as %s" % (c.head, obj.pid)
                # for now, return after ingesting a single object (still testing)
                return

        

