from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import Client, TestCase

User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user_author = User.objects.create_user(
            username='Mr.tester',
            password='123456789'
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(PostURLTests.user_author)

    def test_urls_for_not_authorized_user(self):
        """ Проверяем доступность адресов входа,
        регистрации и востановления пароля для
        неавторизированного прользователя.
        """
        urls_for_not_authorized = [
            '/auth/signup/',
            '/auth/login/',
            '/auth/password_reset/',
            '/auth/password_reset/done/',
            '/auth/logout/',
            '/auth/reset/done/',
            '/auth/reset/f4h45h/this_token_mother/',
        ]
        for url in urls_for_not_authorized:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(
                    response.status_code,
                    HTTPStatus.OK,
                    f'Ненайден адрес:{url}'
                )

    def test_urls_for_authorized_user(self):
        """ Проверяем доступность адресов для авторизированного
        прользователя.
        """
        urls_for_authorized = [
            '/auth/signup/',
            '/auth/password_change/',
            '/auth/password_change/done/',
            '/auth/logout/',
            '/auth/password_reset/',
            '/auth/password_reset/done/',
            '/auth/reset/done/',
            '/auth/login/',
        ]
        for url in urls_for_authorized:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(
                    response.status_code,
                    HTTPStatus.OK,
                    f'Ненайден адрес:{url}'
                )

    def test_redirect_for_not_authorized(self):
        """ Проверяем перенаправление на страницу,
        входа для неавторизированного
        прользователя.
        """
        urls_closed = [
            '/auth/password_change/',
            '/auth/password_change/done/',
        ]
        for url in urls_closed:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                addr_to_redir = f'/auth/login/?next={url}'
                self.assertRedirects(
                    response,
                    addr_to_redir
                )

    def test_open_templates_for_not_authorized(self):
        """ Проверка открытия шаблонов по адресам
        для невошедших пользователей."""
        urls_with_templates = [
            ('/auth/signup/', 'users/signup.html'),
            ('/auth/logout/', 'users/logged_out.html'),
            ('/auth/password_reset/', 'users/password_reset_form.html'),
            ('/auth/password_reset/done/', 'users/password_reset_done.html'),
            ('/auth/reset/f4h45h/this_token_mother/',
                'users/password_reset_confirm.html'),
            ('/auth/reset/done/', 'users/password_reset_complete.html'),
            ('/auth/login/', 'users/login.html')
        ]
        for tuplee in urls_with_templates:
            with self.subTest(url=tuplee[0]):
                response = self.guest_client.get(tuplee[0])
                self.assertTemplateUsed(
                    response,
                    tuplee[1],
                    'Адрес несоответсвует шаблону.'
                )

    def test_open_templates_for_authorized(self):
        """ Проверка открытия шаблонов по адресам для
        авторизированных пользователей."""
        urls_with_templates = [
            ('/auth/signup/', 'users/signup.html'),
            ('/auth/password_change/', 'users/password_change_form.html'),
            ('/auth/password_change/done/', 'users/password_change_done.html'),
            ('/auth/logout/', 'users/logged_out.html'),
            ('/auth/password_reset/', 'users/password_reset_form.html'),
            ('/auth/password_reset/done/', 'users/password_reset_done.html'),
            ('/auth/reset/f4h45h/this_token_mother/',
                'users/password_reset_confirm.html'),
            ('/auth/reset/done/', 'users/password_reset_complete.html'),
            ('/auth/login/', 'users/login.html')
        ]
        for tuplee in urls_with_templates:
            with self.subTest(url=tuplee[0]):
                response = self.authorized_client.get(tuplee[0])
                self.assertTemplateUsed(
                    response,
                    tuplee[1],
                    'Адрес несоответсвует шаблону.'
                )
