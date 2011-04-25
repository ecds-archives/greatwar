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
'''

'''

#FIXME: there should be a better place to put this... (eulcore.fedora somewhere)
MEMBER_OF_COLLECTION = 'info:fedora/fedora-system:def/relations-external#isMemberOfCollection'

class Command(BaseCommand):        
    """Ingest Great War Project postcards from a local source directory into
    a Fedora repository.
    The command to run this script from Alice Hickcoxs computer is:
    ./manage.py ingest_postcards /Beck-files/WWI/greatwar/trunk/xml/postcards/postcards.xml /Volumes/FreeAgent\ Drive/GreatWar/images-fullsize/
    The full size (tiff) images are stored on the external hard drive /Volumes/FreeAgent\ Drive/GreatWar/images-fullsize
    To test the ingest use the --dry-run switch.
    """
    help = __doc__

    option_list = BaseCommand.option_list + (
        make_option('--dry-run', '-n',
            dest='dry_run',
            action='store_true',
            help='''Test the ingest, but don\'t actually do anything.'''),
        )




    args = 'postcards.xml image_dir'
    

    def handle(self, cards_fname, image_dir, dry_run=False, **options):
        verbosity = int(options['verbosity'])    # 1 = normal, 0 = minimal, 2 = all
        v_normal = 1

        #prompt for user and password
        user = raw_input('user:')
        password = raw_input('password:')
        repo = Repository(username=user, password=password)
        collection = PostcardCollection.get()
        if not collection.exists:
            raise Exception(collection.pid + " is not in the repository. Do you need to syncrepo?")

        def anas_simple(my_dict,a):
            for ana in my_dict:
                if ana in a:
                    return my_dict[ana]


#        def anas_complex(a,b):
#            for ana in ana_lcc:
#                if ana not in a:
#                   return FALSE
#                if ana in b:
#                   return ana_lcc[ana] 
    


        #dictionary of lc subjects, simple (using 1 ana id) and complex (using 2 ana ids).
        ana_lcs = {"nat-it":"World War, 1914-1918--Italy",
                   "nat-fr":"World War, 1914-1918--France",
                   "nat-us":"World War, 1914-1918--United States",
                   "nat-de":"World War, 1914-1918--Germany",
                   "nat-brit":"World War, 1914-1918--Great Britain",
                   "nat-bel":"World War, 1914-1918--Belgium",
                   "nat-au":"World War, 1914-1918--Austria",
                   "nat-nl":"World War, 1914-1918--Netherlands",
                   "nat-rus":"World War, 1914-1918--Russia",
                   "nat-jp":" World War, 1914-1918--Japan",
                   "nat-ee":"World War, 1914-1918--Eastern Europe",
                   "nat-ca":"World War, 1914-1918--Canada",
                   "nat-hu":"World War, 1914-1918--Hungary",
                   "mil-nur":"Military Nursing",
                   "con-h":"World War, 1914-1918--Humor", 
                   "con-v":"World War, 1914-1918--Poetry", 
                   "con-p":"World War, 1914-1918--Persons", 
                   "con-m":"World War, 1914-1918--Memorials", 
                   "con-r":"World War, 1914-1918--Destruction  and pillage",
                   "con-f":"Flags in art",
                   "con-el":"Uncle Elmer",
                   "hf-p":"World War, 1914-1918--Propganda", 
                   "hf-c":"World War, 1914-1918--Children", 
                   "hf-w":"World War, 1914-1918--Women", 
                   "hf-re":"World War, 1914-1918--Religious aspects", 
                   "hf-ro":"World War, 1914-1918--Man-Woman relationships",
                        }


        ana_lcc_army = {"nat-fr":u"France. Arm\xe9e", 
                           "nat-brit":"Great Britain. Army", 
                           "nat-bel":u"Belgium. Arm\xe9e", 
                           "nat-de":"Germany. Heer", 
                           "nat-us":"United States. Army", 
                           "nat-ca":"Canada. Canadian Army", 
                           "nat-jp":"Japan. Rikugun", 
                           "nat-au":u"Austria. Arm\xe9e",
                    }
        ana_lcc_navy = {"nat-brit":"Royal Navy. Great Britain", 
                           "nat-us":"United States. Navy", 
                           "nat-fr":"France. Marine", 
                           "nat-de":"Germany. Kriegsmarine", 
                           "nat-ca":"Canada. Royal Canadian Navy",       
                           }
        #images use dc:type
        ana_lcimage  = {"im-ph":"photograph",
                        "im-pa":"painting",
                        "im-dr":"drawing",
                        "im-ca":"cartoon",
                        "im-en":"engraving",
                        "im-po":"poster",
                        "im-s":"silk postcard", 
                        }
        #use dc:coverage
        ana_lccoverage = {"t-wwi":"1914-1918",
                          "t-pre":"Before 1914",
                          "t-post":"After 1918",
                          "t-ww2":"1939-1945",
                          "t-post2":"After 1945",
                          } 
        
        # make a dictionary of subjects so type and value is easily accessible by id
        interps = collection.interp.content.interp_groups
        subjects = {}
        for group in interps:
            for interp in group.interp:
                subjects[interp.id] = (group.type, interp.value)

        cards_tei = load_xmlobject_from_file(cards_fname, xmlclass=Tei)
        cards = cards_tei.body.all_figures
        files = 0
        ingested = 0
        for c in cards:
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
            obj.dc.content.identifier_list.append(c.entity) # Store local identifiers in DC
            obj.label = c.head
            obj.owner = settings.FEDORA_OBJECT_OWNERID
            obj.dc.content.title = obj.label

            #append label so postcard description can be identified in the description elements
            obj.dc.content.description_list.append('%s%s' % (settings.POSTCARD_DESCRIPTION_LABEL, c.description))

            #Add floating text from postcards (text written on the card)
            float_lines = [] # list of lines of text from the postcard
            linegroups = c.floatingText_lg #if text is stored in linegroups use this variable
            lines = c.floatingText_l #if text is only lines w/o linegroup then use this 
            if len(linegroups) > 0:
                for group in linegroups:
                    if group.head is not None: #treat head as normal line
                        float_lines.append(group.head)
                    for line in group.line: #add the rest of the lines
                        float_lines.append(line)
                    float_lines.append('\n') #each linegroup needs an extra \n at the end to make a paragraph
            elif len(lines) > 0:
                for line in lines:
                    float_lines.append(line)
            float_lines = map(unicode, float_lines) #convert all lines to unicode
            float_lines = str.join("\n", float_lines) #Add \n for each line break and convert to a str

            #append label so floating text (postcard text) can be identified in the description elements
            obj.dc.content.description_list.append('%s%s' % (settings.POSTCARD_FLOATINGTEXT_LABEL, float_lines))


            # convert interp text into dc: subjects
            local_subjects = []
            for ana_id in c.ana.split():
                #            ana_id = c.ana.split()
                if ana_id in subjects:
                    local_subjects.append('%s: %s' % subjects[ana_id])
                else:
                    print 'ana id %s not recognized for %s' % (ana_id, c.entity)
            obj.dc.content.subject_list.extend(local_subjects)

            lc_subjects = []
            ana_ids = []
            ana_ids = c.ana.split()
            if verbosity > v_normal:
                print 'DEBUG: %s are the ana ids for %s' % (ana_ids, c.entity) 
            for ana_id in ana_ids:
                if ana_id in ana_lcc_army:
                    for ana_id2 in ana_ids:
                        if  ana_id2 == "mil-a":
                            ana_lc = ana_lcc_army[ana_id]
                            lc_subjects.append('%s' % ana_lc)
                            print '%s added to LC subjects list-army or navy' % ana_lc
                            
                if ana_id in ana_lcc_navy:
                    for ana_id2 in ana_ids:
                        if ana_id2 == "mil-na":
                            ana_lc = ana_lcc_navy[ana_id]
                            lc_subjects.append('%s' % ana_lc)
                            print '%s added to LC subjects list-army or navy' % ana_lc
                if ana_id in ana_lcs:
                    ana_lc = anas_simple(ana_lcs, ana_id)
                    lc_subjects.append('%s' % ana_lc)
                    print '%s added to LC subjects list-nat, mil-nur, con, hf' % (ana_lc)
#                else:         
#                    print 'ana id %s not recognized for %s' % (ana_id, c.entity)
            obj.dc.content.subject_list.extend(lc_subjects)

            for ana_id in ana_ids:
                my_dict = ana_lcimage
                if ana_id in my_dict:
#                    print 'DEBUG %s found in image list' % ana_id
                    ana_image = anas_simple(my_dict, ana_id)
#                    print 'DEBUG %s is the value for %s' % (ana_image, ana_id)
                    lc_subjects.append('%s' % ana_image)
                    print '%s added to LC subjects list-image type' % (ana_image)
#                else:
#                    print 'ana id %s not recognized for %s' % (ana_id, c.entity)
            obj.dc.content.type_list.extend(lc_subjects)       

            for ana_id in ana_ids:
                my_dict = ana_lccoverage
                if ana_id in my_dict:
                    ana_cover = anas_simple(my_dict,ana_id)
                    lc_subjects.append('%s' % ana_cover)
                    print '%s added to LC subjects list-coverage' % ana_cover
#                else:
#                    print 'ana id %s not recognized for %s' % (ana_id, c.entity)
            obj.dc.content.coverage_list.extend(lc_subjects)
            
                
            # common DC for all postcards
            obj.dc.content.type = 'image'
            obj.dc.content.type = 'postcard'
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
        print "Found %d postcards " % len(cards)
        print "Found %d postcard files " % files
        print "Ingested %d postcards " % ingested

        

