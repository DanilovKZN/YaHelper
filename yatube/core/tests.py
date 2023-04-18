from django.test import Client, TestCase


class ViewTestClass(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_error_page(self):
        """Проверяем статус-код = 404?"""
        response = self.guest_client.get('/nonexist-page/')
        self.assertEqual(
            response.status_code, 404,
            f'А вот и нет, пришел код: {response.status_code}')

    def test_error_page_tampletes(self):
        """Проверяем тот ли строится шаблон"""
        response = self.guest_client.get('/nonexist-page/')
        self.assertTemplateUsed(response, 'core/404.html')
