from django.test import TestCase
from django.db.utils import IntegrityError
from rest_framework.permissions import IsAuthenticated

from mooclets.models import Mooclet, BasicMoocletAuthenticator
from backend.utils.mooclet_connector import DUMMY_MOOCLET_URL, DUMMY_MOOCLET_API_TOKEN

class MoocletCreateTestCase(TestCase):
    url = DUMMY_MOOCLET_URL
    token = DUMMY_MOOCLET_API_TOKEN

    def setUp(self):
        self.mooclet_authenticator = BasicMoocletAuthenticator(url=self.url, token=self.token)
        self.mooclet_authenticator.save()

    def test_authenticator(self):
        self.assertEqual(self.mooclet_authenticator.url, self.url)
        self.assertEqual(self.mooclet_authenticator.token, self.token)
        self.assertEqual([IsAuthenticated], self.mooclet_authenticator.get_permission_classes())

    def test_create_mooclet_no_external_id_fails(self):
        with self.assertRaises(IntegrityError):
            mooclet = Mooclet(content_object=self.mooclet_authenticator)
            mooclet.save()

    def test_create_mooclet_no_authenticator_fails(self):
        with self.assertRaises(Exception):
            mooclet = Mooclet(external_id = 1)
            mooclet.save()

    def test_create_moclet_succeeds(self):
        mooclet = Mooclet(external_id=1, content_object = self.mooclet_authenticator)
        mooclet.save()

class MoocletTestCase(TestCase):
    url = DUMMY_MOOCLET_URL
    token = DUMMY_MOOCLET_API_TOKEN

    def setUp(self):
        mooclet_authenticator = BasicMoocletAuthenticator(url=self.url, token=self.token)
        mooclet_authenticator.save()
        self.mooclet = Mooclet(external_id=1, content_object = mooclet_authenticator)
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

