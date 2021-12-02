from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import FieldError
from rest_framework.exceptions import ValidationError

from mooclets.models import Mooclet, BasicMoocletAuthenticator
from mooclets.serializers import CreateMoocletSerializer

class MoocletSerializerTestCase(TestCase):
    url = "http://test_url.com"
    token = "token!"
    name = 'Name'

    def setUp(self):
        self.mooclet_authenticator = BasicMoocletAuthenticator(url=self.url, token=self.token)
        self.mooclet_authenticator.save()

    def test_create(self):
        data = {
                'name': self.name,
                'external_id': 1,
                }
        serializer = CreateMoocletSerializer(data=data, context = {"mooclet_authenticator": self.mooclet_authenticator})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        mooclet = Mooclet.objects.get(name=self.name)
        self.assertEqual(mooclet.token, self.token)
        self.assertEqual(mooclet.url, self.url)

    def test_create_mooclet_wrong_authenticator_fails(self):
        wrong_auth = Mooclet(external_id=1, content_object = self.mooclet_authenticator)
        wrong_auth.save()

        data = {
                'name': self.name,
                'external_id': 1,
                }

        serializer = CreateMoocletSerializer(data=data, context = {"mooclet_authenticator": wrong_auth})
        with self.assertRaises(ValueError):
            serializer.is_valid(raise_exception=True)
            serializer.save()
            

    def test_create_two_same_mooclets_fails(self):
        data1 = {
                'name': self.name,
                'external_id': 1,
                }
        data2 = {
                'name': self.name,
                'external_id': 1,
                }

        serializer1 = CreateMoocletSerializer(data=data1, context = {"mooclet_authenticator": self.mooclet_authenticator})
        serializer1.is_valid(raise_exception=True)
        serializer1.save()

        serializer2 = CreateMoocletSerializer(data=data2, context = {"mooclet_authenticator": self.mooclet_authenticator})

        with self.assertRaises(ValidationError):
            serializer2.is_valid(raise_exception=True)
            serializer2.save()


