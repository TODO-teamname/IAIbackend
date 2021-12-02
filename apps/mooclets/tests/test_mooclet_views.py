from django.test import TestCase
from rest_framework.permissions import IsAuthenticated
from rest_framework.test import APIRequestFactory, force_authenticate

from mooclets.models import Mooclet, BasicMoocletAuthenticator
from mooclets.views import MoocletViewSet
from django.contrib import auth
from backend.utils.mooclet_connector import DUMMY_MOOCLET_URL, DUMMY_MOOCLET_API_TOKEN

class MoocletViewTestCase(TestCase):
    valid_external_id=3
    invalid_external_id=2
    def setUp(self):
        self.factory = APIRequestFactory()
        actions = {
            'get': 'retrieve'}
        self.view = MoocletViewSet.as_view(actions)

        self.user = auth.get_user_model()(email="test@gmail.com", password="password", first_name="Test", last_name="User")

        authenticator = BasicMoocletAuthenticator(url=DUMMY_MOOCLET_URL, token=DUMMY_MOOCLET_API_TOKEN)
        authenticator.save()

        mooclet = Mooclet(external_id=self.valid_external_id, content_object=authenticator)
        mooclet.save()
        self.mooclet_id = mooclet.id

    def test_get(self):
        mooclet = Mooclet.objects.get(id=self.mooclet_id)
        data = {}

        request = self.factory.get('/mooclets/')
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=self.mooclet_id)

        expected_response_data = {'id': self.mooclet_id, 'external_id': self.valid_external_id}


        self.assertEqual(response.data['id'], self.mooclet_id)
        self.assertEqual(response.data['external_id'], self.valid_external_id)
        self.assertIn('name', response.data)
