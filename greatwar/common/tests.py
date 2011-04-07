from django.test import TestCase
from django.conf import settings
from django.core.urlresolvers import reverse
from greatwar.common.utils import get_pid_target, absolutize_url

class UtilsTest(TestCase):

    #used to save real settings
    _BASE_URL = None
    _FEDORA_PIDSPACE = None

    def setUp(self):
        #save old values and assign test values
        self.__BASE_URL = settings.BASE_URL
        self._FEDORA_PIDSPACE = settings.FEDORA_PIDSPACE

        settings.BASE_URL = 'http:/myurl.com'
        settings.FEDORA_PIDSPACE = 'test-pidspace' 


    def tearDown(self):
        settings.BASE_URL = self._BASE_URL
        settings.FEDORA_PIDSPACE = self._FEDORA_PIDSPACE


    def test_get_pid_target(self):
        target = get_pid_target('postcards:card')
        expected = '%s/postcards/%s:%s' %(settings.BASE_URL, settings.FEDORA_PIDSPACE, settings.PID_TOKEN)
        self.assertEqual(target,expected)
