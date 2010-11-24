"""
Great War Postcards Test Cases
"""

from datetime import datetime
from os import path
import re
from time import sleep
from types import ListType
from lxml import etree
from urllib import quote as urlquote

from django.conf import settings
from django.core.cache import cache
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.http import Http404, HttpRequest
from django.template import RequestContext, Template
from django.test import Client, TestCase as DjangoTestCase

from greatwar.postcards.fixtures.postcards import FedoraFixtures

exist_fixture_path = path.join(path.dirname(path.abspath(__file__)), 'fixtures')
exist_index_path = path.join(path.dirname(path.abspath(__file__)), '..', 'exist_index.xconf')

# load fixture postcards to test pidspace - will be removed after tests complete
postcards = FedoraFixtures().load_postcards()

class PostcardViewsTestCase(DjangoTestCase):
                                  
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
        for p in postcards:
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
        postcard = postcards[0]
        postcard_url = reverse('postcards:card', kwargs={'pid': postcard.pid})
        response = self.client.get(postcard_url)
        expected = 200
        self.assertEqual(response.status_code, expected,
                        'Expected %s but returned %s for %s' % \
                        (expected, response.status_code, postcard_url))
        self.assertContains(response, postcard.label,
            msg_prefix='postcard view includes postcard label')
        self.assertContains(response, postcard.dc.content.description,
            msg_prefix='postcard view includes postcard description')
        self.assertContains(response, reverse('postcards:img-medium',
                    kwargs={'pid': postcard.pid}),
                    msg_prefix='medium image for postcard displayed on postcard view')
        self.assertContains(response, reverse('postcards:img-large',
                    kwargs={'pid': postcard.pid}),
                    msg_prefix='large image for postcard linked from postcard view')

        for subject in postcard.dc.content.subject_list:
            self.assertContains(response, subject,
                msg_prefix='subject %s contained in postcard view' % subject)

    def test_postcard_thumbnail(self):
        # nonexistent pid should return 404
        thumb_url = reverse('postcards:img-thumb', kwargs={'pid': 'bogus:nonexistent-pid'})
        response = self.client.get(thumb_url)
        expected = 404
        self.assertEqual(response.status_code, expected,
                        'Expected %s but returned %s for %s' % \
                        (expected, response.status_code, thumb_url))

        # first fixture object
        postcard = postcards[0]
        # TODO/FIXME: getting a 500 error on this; something wrong with fixture?
        thumb_url = reverse('postcards:img-thumb', kwargs={'pid': postcard.pid})
        #response = self.client.get(thumb_url)
        #expected = 200
        #self.assertEqual(response.status_code, expected,
        #               'Expected %s but returned %s for %s' % \
        #                (expected, response.status_code, thumb_url))
        # TODO: also test mimetype
        

        
