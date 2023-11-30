from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class TestSportType(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_sport_type_list(self):
        url = reverse('api:sport_types-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestSearchListApi(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_search_sections_list(self):
        url = reverse('api:search_sections-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
