import os

from django.conf import settings
from django.core.management.base import BaseCommand

from eulcore.django.fedora.server import Repository

from greatwar.postcards.models import ImageObject, Postcard, Categories

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
        interps = Categories.objects.all()
        # make a dictionary of subjects so type and value is easily accessible by id
        subjects = {}
        for group in interps:
            for interp in group.interp:
                subjects[interp.id] = (group.type, interp.value)

        cards = Postcard.objects.all()
        ingested = 0
        for c in cards:
            file = os.path.join(settings.MASTERS_SOURCE, 'wwi_%s.tif' % c.entity)
            if os.access(file, os.F_OK):
                print "Found master file %s for %s" % (file, c.entity)
                obj = repo.get_object(type=ImageObject)
                obj.label = c.head
                obj.owner = 'smallpox'      # hack - take advantage of GHC xacml policy for now, for simplicity
                obj.dc.content.title = obj.label                
                obj.dc.content.description = c.description
                # convert interp text into dc: subjects
                obj.dc.content.subject_list.extend(['%s: %s' % subjects[ana_id]
                                                    for ana_id in c.ana.split(' ')])

                # common DC for all postcards
                obj.dc.content.type = 'image'
                obj.dc.content.relation_list.extend(['The Great War 1914-1918',
                                     'http://beck.library.emory.edu/greatwar/'])
            
                obj.image.content = open(file)
                obj.save()
                print "ingested %s as %s" % (c.head, obj.pid)
                ingested += 1


        # summarize what was done
        print "Found %d postcards " % cards.count()
        print "Ingested %d postcards " % ingested

        

