from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import FieldError
from rest_framework.exceptions import ValidationError
from organizations.models import Organization

from mooclets.models import Mooclet, BasicMoocletAuthenticator
from mooclets.serializers import CreateMoocletSerializer

class OrganizationMoocletAuthenticatorTestCase(TestCase):
    url = "url!"
    token = "token!"
    name = "Name!"

    def setUp(self):
        organization = Organization(name = self.name, url = self.url, token = self.token)
        organization.save()
        self.organization = organization

    def test_authenticator(self):
        authenticator = self.organization.mooclet_authenticator
        self.assertEqual(authenticator.get_url(), self.url)
        self.assertEqual(authenticator.get_token(), self.token)
