from django.test import TestCase, Client


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_sport_type_list_url(self):
        response = self.guest_client.get('/api/sport_types/')
        self.assertEqual(response.status_code, 200)

    def test_search_section_list_url(self):
        response = self.guest_client.get('/api/search_sections/')
        self.assertEqual(response.status_code, 200)
