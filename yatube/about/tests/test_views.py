from django.test import Client, TestCase
from django.urls import reverse


class AboutPagesTests(TestCase):

    def setUp(self):
        self.guest_client = Client()

    def test_uses_correct_templates_for_authirized(self):
        """ Проверяем соответсвие адресов и вызываемых
        шаблонов для авторизированного пользователя"""
        urls_templates = {
            reverse('about:author'): 'about/author.html',
            reverse('about:tech'): 'about/tech.html',
        }
        for reverse_name, template in urls_templates.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.guest_client.get(reverse_name)
                self.assertTemplateUsed(
                    response,
                    template,
                    'Адресс не соответствует шаблону.'
                )
