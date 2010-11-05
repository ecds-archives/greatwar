from optparse import make_option
import os
import sys

from rdflib import URIRef
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from eulcore.django.fedora.server import Repository
from eulcore.xmlmap import load_xmlobject_from_file
from eulcore.xmlmap.teimap import Tei

from greatwar.postcards.models import ImageObject, Postcard, Categories, PostcardCollection

#FIXME: there should be a better place to put this... (eulcore.fedora somewhere)
MEMBER_OF_COLLECTION = 'info:fedora/fedora-system:def/relations-external#isMemberOfCollection'

class Command(BaseCommand):        
    """Ingest Great War Project postcards from a local source directory into
    a Fedora repository.
    """
    help = __doc__

    option_list = BaseCommand.option_list + (
        make_option('--dry-run', '-n',
            dest='dry_run',
            action='store_true',
            help='''Test the ingest, but don't actually do anything.'''),
        )

    args = 'postcards.xml image_dir'

    def handle(self, cards_fname, image_dir, dry_run=False, **options):
        verbosity = int(options['verbosity'])    # 1 = normal, 0 = minimal, 2 = all
        v_normal = 1

        repo = Repository()
        collection = repo.get_object('greatwar:postcards-collection',
                                    type=PostcardCollection)
        if not collection.exists:
            raise Exception("greatwar:postcards-collection is not in the repository. Do you need to syncrepo?")

        # make a dictionary of subjects so type and value is easily accessible by id
        interps = collection.interp.content.interp_groups
        subjects = {}
        for group in interps:
            for interp in group.interp:
                subjects[interp.id] = (group.type, interp.value)

        cards_tei = load_xmlobject_from_file(cards_fname, xmlclass=Tei)
        files = 0
        ingested = 0
        for c in cards_tei.body.all_figures:
            file = os.path.join(image_dir, '%s.tif' % c.entity)
            if os.access(file, os.F_OK):
                if verbosity >= v_normal:
                    print "Found master file %s for %s" % (file, c.entity)
            else:
                file = os.path.join(image_dir, 'wwi_%s.tif' % c.entity)
                if os.access(file, os.F_OK):
                    if verbosity >= v_normal:
                        print "Found master file %s for %s" % (file, c.entity)
                else:
                    if verbosity >= v_normal:
                        print "File not found for %s" % c.entity
                    continue

            files += 1
            
            obj = repo.get_object(type=ImageObject)
            obj.label = c.head
            obj.owner = settings.FEDORA_OBJECT_OWNERID
            obj.dc.content.title = obj.label
            obj.dc.content.description = c.description
            # TODO: handle postcards with text/poetry lines

            # convert interp text into dc: subjects
            obj.dc.content.subject_list.extend(['%s: %s' % subjects[ana_id]
                                                for ana_id in c.ana.split()])

            # common DC for all postcards
            obj.dc.content.type = 'image'
            obj.dc.content.relation_list.extend(['The Great War 1914-1918',
                                 'http://beck.library.emory.edu/greatwar/'])

            # set file as content of image datastream
            obj.image.content = open(file)

            # add relation to postcard collection
            obj.rels_ext.content.add((
                        URIRef(obj.uri),
                        URIRef(MEMBER_OF_COLLECTION),
                        URIRef(PostcardCollection.get().uri)
                ))
            # TODO: OAI identifier ?

            if verbosity > v_normal:
                print "Dublin Core\t\n", obj.dc.content.serialize(pretty=True)
                print "RELS-EXT \t\n", obj.rels_ext.content.serialize(pretty=True)
            
            if not dry_run:
                obj.save()
            print "ingested %s as %s" % (unicode(c.head).encode('latin-1'), obj.pid)
            ingested += 1


        # summarize what was done
        print "Found %d postcards " % cards.count()
        print "Found %d postcard files " % files
        print "Ingested %d postcards " % ingested

        

