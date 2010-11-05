from os import path
from rdflib import URIRef

from django.conf import settings
from eulcore.django.fedora.server import Repository

from greatwar.postcards.models import ImageObject, PostcardCollection

fixture_path = path.dirname(path.abspath(__file__))
 # FIXME: there should be a better place to put this... (eulcore.fedora somewhere?)
MEMBER_OF_COLLECTION = 'info:fedora/fedora-system:def/relations-external#isMemberOfCollection'


class FedoraFixtures:
    # class to load postcard fixtures to repo for unit tests
    postcards = []

    def _load_postcard(self, label, description, subjects, filename):
        '''Create a postcard object and load to fedora.

        :param label: object label and dc:title
        :param description: object dc:description
        :param subjects: list of subjects to be set in dc:subject
        :param filename: filename for image content, assumed relative to current directory
        '''
        # NOTE: image object init here somewhat redundant with current postcard ingest logic
        repo = Repository()
        obj = repo.get_object(type=ImageObject)
        obj.label = label
        obj.owner = settings.FEDORA_OBJECT_OWNERID
        obj.dc.content.title = obj.label
        obj.dc.content.description = description
        obj.dc.content.subject_list.extend(subjects)
        # common DC for all postcards
        obj.dc.content.type = 'image'
        # FIXME: configure this somewhere?
        obj.dc.content.relation_list.extend(['The Great War 1914-1918',
                                 'http://beck.library.emory.edu/greatwar/'])
        # set file as content of image datastream
        obj.image.content = open(path.join(fixture_path, filename))
        # add relation to postcard collection
        obj.rels_ext.content.add((
                    URIRef(obj.uri),
                    URIRef(MEMBER_OF_COLLECTION),
                    URIRef(PostcardCollection.get().uri)
            ))
        obj.save()
        self.postcards.append(obj)

    def load_postcards(self):
        'Load postcard fixture object and return a list of the objects.'
        
        self._load_postcard('Boys at Mess,- Camp Sherman, Chillicothe, Ohio.',
            'soldiers at mess',
            ['time period: during Great War', 'image: photo', 'military: Army',
            'nationality: United States'],
            'Sherman_mess.jpg')
        self._load_postcard('Sailor', 'black and white photo of a sailor in white',
            ['time period: during Great War', 'image: photo', 'military: Navy',
            'nationality: United States'],
            'knee_up_sailor.jpg')
        self._load_postcard('Kieler Woche 1911', 'four ships in the water',
            ['time period: pre Great War', 'image: photo', 'military: Navy',
            'nationality: Germany'],
            'Kieler_Woche_1911.jpg')

        return self.postcards
