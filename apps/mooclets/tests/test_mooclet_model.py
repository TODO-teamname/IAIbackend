from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import FieldError
from rest_framework.permissions import IsAuthenticated

from mooclets.models import Mooclet, BasicMoocletAuthenticator
from mooclets.utils.mooclet_connector import MoocletConnector

class MoocletCreateTestCase(TestCase):
    url = "url!"
    token = "token!"

    def setUp(self):
        self.mooclet_authenticator = BasicMoocletAuthenticator(url=self.url, token=self.token)
        self.mooclet_authenticator.save()

    def test_authenticator(self):
        self.assertEqual(self.mooclet_authenticator.url, self.url)
        self.assertEqual(self.mooclet_authenticator.token, self.token)
        self.assertEqual([IsAuthenticated], self.mooclet_authenticator.get_permission_classes())

    def test_create_mooclet_no_external_id_fails(self):
        with self.assertRaises(IntegrityError):
            mooclet = Mooclet(authenticator_object=self.mooclet_authenticator)
            mooclet.save()

    def test_create_mooclet_no_authenticator_fails(self):
        with self.assertRaises(FieldError):
            mooclet = Mooclet(external_id = 1)
            mooclet.save()

    def test_create_mooclet_non_authenticator_fails(self):
        wrong_auth = Mooclet(external_id=1, authenticator_object = self.mooclet_authenticator)
        wrong_auth.save()
        with self.assertRaises(FieldError):
            mooclet = Mooclet(external_id=1, authenticator_object = wrong_auth)
            mooclet.save()

    def test_create_moclet_succeeds(self):
        mooclet = Mooclet(external_id=1, authenticator_object = self.mooclet_authenticator)
        mooclet.save()

class MoocletTestCase(TestCase):
    url = "http://test_url.com"
    token = "token!"

    def setUp(self):
        mooclet_authenticator = BasicMoocletAuthenticator(url=self.url, token=self.token)
        mooclet_authenticator.save()
        self.mooclet = Mooclet(external_id=1, authenticator_object = mooclet_authenticator)
        self.mooclet.save()

    def test_url(self):
        self.assertEqual(self.mooclet.url, self.url)

    def test_token(self):
        self.assertEqual(self.mooclet.token, self.token)

    def test_get_permission_classes(self):
        self.assertEqual(self.mooclet.get_permission_classes(), [IsAuthenticated])


    """def test_get_connector(self):
        self.assertEqual(self.mooclet.get_connector(), MoocletConnector)
    """


            
    
