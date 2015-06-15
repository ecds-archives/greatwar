"""
Great War Postcards Test Cases
"""

from os import path

from django.core.urlresolvers import reverse
from django.test import TestCase as DjangoTestCase
from django.conf import settings

from eulfedora.server import Repository

from greatwar.postcards.fixtures.postcards import FedoraFixtures
from util import get_pid_target, absolutize_url
from pidservices.djangowrapper.shortcuts import DjangoPidmanRestClient

exist_fixture_path = path.join(path.dirname(path.abspath(__file__)), 'fixtures')
exist_index_path = path.join(path.dirname(path.abspath(__file__)), '..', 'exist_index.xconf')



class PostcardViewsTestCase(DjangoTestCase):
    repo = Repository()

    # load fixture postcards to test pidspace
    postcards = FedoraFixtures().load_postcards()


    def __del__(self):
        for p in self.postcards:
            self.repo.purge_object(p.pid)


    def test_index(self):
        "Test postcard index/about page"
        about_url = reverse('postcards:index')
        response = self.client.get(about_url)
        expected = 200
        self.assertEqual(response.status_code, expected,
                        'Expected %s but returned %s for %s' % \
                        (expected, response.status_code, about_url))

        self.assertContains(response, reverse('postcards:browse'),
            msg_prefix='postcard index page includes link to postcard browse')
        self.assertContains(response, reverse('postcards:search'),
            msg_prefix='postcard index page includes link to postcard search')
        # NOTE: currently, count may get off if tests fail and fixtures are not removed
        self.assertContains(response, 'browse through all <b>3</b> postcards',
            msg_prefix='postcard index page includes total postcard count')
        # should contain one random postcard  - how to test?

    def test_browse(self):
        'Test postcard browse page'

        browse_url = reverse('postcards:browse')
        response = self.client.get(browse_url)
        expected = 200
        self.assertEqual(response.status_code, expected,
                        'Expected %s but returned %s for %s' % \
                        (expected, response.status_code, browse_url))

        # all fixture objects should on browse page
        for p in self.postcards:
            self.assertContains(response, reverse('postcards:card',
                    kwargs={'pid': p.pid}),
                    msg_prefix='link to postcard fixture %s should be linked from browse page' % p.pid)
            self.assertContains(response, reverse('postcards:img-thumb',
                    kwargs={'pid': p.pid}),
                    msg_prefix='thumbnail image for postcard fixture %s displayed on browse page' % p.pid)
            self.assertContains(response, p.label,
                    msg_prefix='label from postcard fixture %s should be listed on browse page' % p.pid)

    def test_view_postcard(self):
        'Test single-postcard view page.'

        # nonexistent pid should return 404
        postcard_url = reverse('postcards:card', kwargs={'pid': 'bogus:nonexistent-pid'})
        response = self.client.get(postcard_url)
        expected = 404
        self.assertEqual(response.status_code, expected,
                        'Expected %s but returned %s for %s' % \
                        (expected, response.status_code, postcard_url))

        # first fixture object
        postcard = self.postcards[0]
        postcard_url = reverse('postcards:card', kwargs={'pid': postcard.pid})
        response = self.client.get(postcard_url)
        expected = 200
        self.assertEqual(response.status_code, expected,
                        'Expected %s but returned %s for %s' % \
                        (expected, response.status_code, postcard_url))
        self.assertContains(response, postcard.label,
            msg_prefix='postcard view includes postcard label')
        self.assertContains(response, postcard.dc.content.description[len(settings.POSTCARD_DESCRIPTION_LABEL):],
            msg_prefix='postcard view includes postcard description')
        self.assertContains(response, reverse('postcards:img-medium',
                    kwargs={'pid': postcard.pid}),
                    msg_prefix='medium image for postcard displayed on postcard view')
        self.assertContains(response, reverse('postcards:card-large',
                    kwargs={'pid': postcard.pid}),
                    msg_prefix='large image for postcard linked from postcard view')



        #Test for floating text
        self.assertContains(response, "Text on postcard:", msg_prefix='Text on postcard heading is present')
        self.assertContains(response, 'This is some floating text', msg_prefix='floating text is present')

        #Test for permanent link
        self.assertContains(response, "Permanent link for this postcard:", msg_prefix='bookmark text')
        self.assertContains(response, postcard.dc.content.identifier_list[0], msg_prefix='bookmark url')

        # DC metadata in header
        self.assertContains(response, '<meta name="DC.title" content="%s" />' % \
            postcard.dc.content.title)
        self.assertContains(response, '<meta name="DC.subject" content="%s" />' % \
            postcard.dc.content.subject)
        self.assertContains(response, '<meta name="DC.type" content="%s" />' % \
            postcard.dc.content.type)

        for subject in postcard.dc.content.subject_list:
            self.assertContains(response, subject,
                msg_prefix='subject %s contained in postcard view' % subject)

    def test_view_postcard_large(self):
            'Test large view page.'

            # page with large postcard display
            postcard = self.postcards[0]
            postcard_url = reverse('postcards:card-large', kwargs={'pid': postcard.pid})
            response = self.client.get(postcard_url)
            expected = 200
            self.assertEqual(response.status_code, expected,
                            'Expected %s but returned %s for %s' % \
                            (expected, response.status_code, postcard_url))

            self.assertContains(response, 'View full details', msg_prefix='View full details text exists')
            self.assertContains(response, reverse('postcards:img-large', kwargs={'pid': postcard.pid}),
                    msg_prefix='large image for postcard on page')


    def test_postcard_thumbnail(self):
        # nonexistent pid should return 404
        thumb_url = reverse('postcards:img-thumb', kwargs={'pid': 'bogus:nonexistent-pid'})
        response = self.client.get(thumb_url)
        expected = 404
        self.assertEqual(response.status_code, expected,
                        'Expected %s but returned %s for %s' % \
                        (expected, response.status_code, thumb_url))

        # first fixture object
        postcard = self.postcards[0]
        # TODO/FIXME: getting a 500 error on this; something wrong with fixture?
        thumb_url = reverse('postcards:img-thumb', kwargs={'pid': postcard.pid})
        #response = self.client.get(thumb_url)
        #expected = 200
        #self.assertEqual(response.status_code, expected,
        #               'Expected %s but returned %s for %s' % \
        #                (expected, response.status_code, thumb_url))
        # TODO: also test mimetype


class UtilTest(DjangoTestCase):

   def test_get_pid_target(self):
       target = get_pid_target('postcards:card')
       expected = '%s/postcards/%s:%s' %(settings.BASE_URL, settings.FEDORA_PIDSPACE, DjangoPidmanRestClient.pid_token)
       self.assertEqual(target,expected)



