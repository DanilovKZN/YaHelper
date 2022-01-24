from django.test import TestCase, Client


class ViewTestClass(TestCase):
    def setUp(self):
        self.guest_client = Client()

    # Проверяем статус-код = 404?
    def test_error_page(self):
        response = self.guest_client.get('/nonexist-page/')
        self.assertEqual(
            response.status_code, 404,
            f'А вот и нет, пришел код: {response.status_code}')

    # Проверяем тот ли строится шаблон
    def test_error_page_tampletes(self):
        response = self.guest_client.get('/nonexist-page/')
        self.assertTemplateUsed(response, 'core/404.html')
