"""
Great War Poetry Test Cases
"""
from os import path

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase as DjangoTestCase

from eulcore.xmlmap  import load_xmlobject_from_file, load_xmlobject_from_string
from eulcore.django.test import TestCase

from greatwar.poetry.models import PoetryBook, Poet


exist_fixture_path = path.join(path.dirname(path.abspath(__file__)), 'fixtures')
exist_index_path = path.join(path.dirname(path.abspath(__file__)), '..', 'collection.xconf')

class PoetryTestCase(DjangoTestCase):
    # tests for poetry model objects

    FIXTURES = ['flower.xml', 'fiery.xml', 'lest.xml']
    POET_STRING = '''<choice xmlns="http://www.tei-c.org/ns/1.0">
        <reg>Peterson, Margaret</reg>
    </choice>'''

    def setUp(self):
      
        # load the three xml poetry objects    
        self.poetry = dict()
        for file in self.FIXTURES:    
          filebase = file.split('.')[0]       
          self.poetry[filebase] = load_xmlobject_from_file(path.join(exist_fixture_path,
                                file), PoetryBook)                                                  
        # load the poet fixture docAuthor
        self.poet = load_xmlobject_from_string(self.POET_STRING, Poet)
                                  
    def test_init(self):
        for file, p in self.poetry.iteritems():   
            self.assert_(isinstance(p, PoetryBook))
          
    def test_xml_fixture_load(self):
        self.assertEqual(3, len(self.poetry))    
      
    def test_poet_attributes(self):    
        self.assertEqual(self.poet.first_letter, 'P')
        self.assertEqual(self.poet.name, 'Peterson, Margaret')
        
class PoetryViewsTestCase(TestCase):
    # tests for ONLY those views that do NOT require eXist full-text index
    exist_fixtures = {'directory' : exist_fixture_path }
    
    def test_index(self):
        # poetry index should list all volumes loaded
        books_url = reverse('poetry:books')
        response = self.client.get(books_url)
        expected = 200
        self.assertEqual(response.status_code, expected,
                        'Expected %s but returned %s for %s' % \
                        (expected, response.status_code, books_url))
        # should contain title, author, link for each fixture
        self.assertContains(response, 'THE FIERY CROSS',
            msg_prefix='poetry index includes title of "The Fiery Cross"')
        self.assertContains(response, 'Mabel C. Edwards',
            msg_prefix='poetry index includes editor of "The Fiery Cross"')
        self.assertContains(response, reverse('poetry:book-toc', args=['fiery']),
            msg_prefix='poetry index includes link to "The Fiery Cross"')
        self.assertContains(response, 'Flower of Youth: Poems in War Time',
            msg_prefix='poetry index includes title of "Flower of Youth"')
        self.assertContains(response, 'Katharine Tynan',
            msg_prefix='poetry index includes author of "Flower of Youth"')
        self.assertContains(response, reverse('poetry:book-toc', args=['flower']),
            msg_prefix='poetry index includes link to "Flower of Youth"')
        self.assertContains(response, 'Lest We Forget',
            msg_prefix='poetry index includes title of "Lest we Forget')
        self.assertContains(response, 'H. B. Elliot',
            msg_prefix='poetry index includes editor of "Lest we Forget')
        self.assertContains(response, reverse('poetry:book-toc', args=['elliot']),
            msg_prefix='poetry index includes link to "Lest we Forget')

    def test_book_toc(self):
         # book toc should list all poems in a book
        book_toc_url = reverse('poetry:book-toc', args=['fiery'])
        response = self.client.get(book_toc_url)
        expected = 200
        self.assertEqual(response.status_code, expected,
                        'Expected %s but returned %s for %s' % \
                        (expected, response.status_code, book_toc_url))
        # should contain title, author, link for each poem
        # - first poem
        self.assertContains(response, 'For the Red Cross',
            msg_prefix='book ToC for fiery includes of "For the Red Cross" (first poem)')
        self.assertContains(response, 'Owen Seaman',
            msg_prefix='book ToC for fiery includes Owen Seaman,  author of ' +
                '"For the Red Cross" (first poem)')
        self.assertContains(response, reverse('poetry:poem', args=['fiery', 'fiery005']),
            msg_prefix='book ToC for fiery includes link to "For the Red Cross" (first poem)')
        # - poem in the middle somewhere
        self.assertContains(response, 'Gifts',      # currently ToC does not list second head
            msg_prefix='book ToC for fiery includes of "Gifts"')
        self.assertContains(response, 'Mary Booth',
            msg_prefix='book ToC for fiery includes Mary Booth,  author of Gifts')
        self.assertContains(response, reverse('poetry:poem', args=['fiery', 'fiery030']),
            msg_prefix='book ToC for fiery includes link to "Gifts"')
        # - last poem
        self.assertContains(response, u'Aux Po\xe8tes Futurs',
            msg_prefix='book ToC for fiery includes of "Aux Poetes Futurs" (last poem)')
        self.assertContains(response, 'Sully Prudhomme',
            msg_prefix='book ToC for fiery includes Sully Prudhomme,  author of ' +
                'Aux Poetes Futurs" (last poem)')
        self.assertContains(response, reverse('poetry:poem', args=['fiery', 'fiery069']),
            msg_prefix='book ToC for fiery includes link to "Aux Poetes Futurs" (last poem)')


        # toc for non-existent book should 404
        book_toc_url = reverse('poetry:book-toc', args=['nonexistent'])
        response = self.client.get(book_toc_url)
        expected = 404
        self.assertEqual(response.status_code, expected,
                        'Expected %s but returned %s for %s' % \
                        (expected, response.status_code, book_toc_url))


class FullTextPoetryViewsTest(TestCase):
    # tests for views that require eXist full-text index
    exist_fixtures = {'index' : settings.EXISTDB_INDEX_CONFIGFILE,
                       'directory' : exist_fixture_path }

    def test_view_search_keyword(self):
        search_url = reverse('poetry:search')

        # TODO: test/cleanup form display - shouldn't complain about no search terms,
        # 0 results when user hasn't entered a query

        response = self.client.get(search_url, {'keyword': 'spectre'})
        expected = 200
        self.assertEqual(response.status_code, expected,
                        'Expected %s but returned %s for %s' % \
                        (expected, response.status_code, search_url))
        
        self.assertContains(response, reverse('poetry:poem', kwargs={'doc_id':'fiery',
            'div_id': 'fiery012'}),
            msg_prefix='search results include link to poem with match (fiery012)')
        self.assertContains(response, 'From Germany',
            msg_prefix='search results include title of poem with match')
        self.assertContains(response, reverse('poetry:book-toc', kwargs={'doc_id':'fiery'}),
            msg_prefix='search results include link to book that contains poem with match')
        self.assertContains(response, 'Pale <span class="exist-match">spectre</span>',
            msg_prefix='search results include poem line with search term highlighted')

        # TODO: also matches fiery004 with title of 'None' - fix title display, test

        # exact phrase search - should work in poem line matches
        response = self.client.get(search_url, {'keyword': '"pale spectre"'})
        expected = 200
        self.assertEqual(response.status_code, expected,
                        'Expected %s but returned %s for %s' % \
                        (expected, response.status_code, search_url))
        self.assertContains(response, '<span class="exist-match">Pale spectre</span> of the slain',
            msg_prefix='search results include poem line with exact phrase search term highlighted')


    def test_view_search_title(self):
        search_url = reverse('poetry:search')
        response = self.client.get(search_url, {'title': 'Germany'})
        expected = 200
        self.assertEqual(response.status_code, expected, 'Expected %s but returned %s for %s' % \
                        (expected, response.status_code, search_url))
        # should include link to fiery012
        self.assertContains(response, reverse('poetry:poem',
                    kwargs={'doc_id':'fiery', 'div_id': 'fiery012'}),
            msg_prefix='search results include link to poem with match')

        # includes link to containing book
        self.assertContains(response, reverse('poetry:book-toc', kwargs={'doc_id':'fiery'}),
            msg_prefix='search results include link to book that contains poem with match')

        # correct title apears in search results
        self.assertContains(response, "From Germany")

    def test_view_search_author(self):
        search_url = reverse('poetry:search')
        response = self.client.get(search_url, {"author" : "Binyon"})
        expected = 200
        self.assertEqual(response.status_code, expected,
                        'Expected %s but returned %s for %s' % \
                        (expected, response.status_code, search_url))

        #Result 1
        #Should include link to fiery014
        self.assertContains(response, reverse('poetry:poem', kwargs={'doc_id':'fiery', 'div_id': 'fiery014'}),
            msg_prefix='search results include link to poem with match)')

        #includes link to containing book
        self.assertContains(response, reverse('poetry:book-toc', kwargs={'doc_id':'fiery'}),
            msg_prefix='search results include link to book that contains poem with match')

        #correct title apears in searh results
        self.assertContains(response, "The Cause")

        #Result 2
        #Should include link to elliott005
        self.assertContains(response, reverse('poetry:poem', kwargs={'doc_id':'elliot', 'div_id': 'elliott005'}),
            msg_prefix='search results include link to poem with match)')

        #includes link to containing book
        self.assertContains(response, reverse('poetry:book-toc', kwargs={'doc_id':'elliot'}),
            msg_prefix='search results include link to book that contains poem with match')

        #correct title apears in searh results
        self.assertContains(response, 'ODE')
