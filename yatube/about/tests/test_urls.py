from django.test import TestCase, Client


class StaticURLTests(TestCase):

    def setUp(self):
        self.guest_client = Client()

    def test_about_urls(self):
        """Проверка доступности адресов."""
        url_to_go = [
            '/about/author/',
            '/about/tech/',
        ]
        for url in url_to_go:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(
                    response.status_code,
                    200,
                    'Пришел другой статус.'
                )

    def test_about_templates(self):
        """Проверка шаблона для адреса."""
        url_and_templates = {
            '/about/author/': 'about/author.html',
            '/about/tech/': 'about/tech.html',
        }
        for url, templates in url_and_templates.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertTemplateUsed(
                    response,
                    templates,
                    'Адресс не соответствует шаблону.'
                )
