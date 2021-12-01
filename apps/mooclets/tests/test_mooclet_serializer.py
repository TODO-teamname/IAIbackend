from django.test import TestCase
from django.db.utils import IntegrityError
from rest_framework.permissions import IsAuthenticated
from mooclets.models import Mooclet, BasicMoocletAuthenticator
from mooclets.utils.mooclet_connector import MoocletConnector
