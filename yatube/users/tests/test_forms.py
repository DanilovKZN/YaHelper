from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class UsersCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаем нового пользователя
        cls.user = User.objects.create(
            username='Vinni Stuh',
            email='Vinni@stuh.ru',
            password='123456789qw',
        )

    def setUp(self):
        self.guest_client = Client()

    # Регистрируем нового пользователя
    def test_signup(self):
        """Заполняем форму Signup для нового пользователя"""
        users_count = User.objects.count()
        forms_dates = {
            'username': 'G514',
            'password1': '987654321qw',
            'password2': '987654321qw',
        }

        response = self.guest_client.post(
            reverse('users:signup'),
            data=forms_dates,
            follow=True
        )

        # Осуществляется ли переход на главную страницу, после регистрации
        self.assertRedirects(response, reverse('posts:index'))

        # Проверяем, изменилось ли количество пользователей
        users_count += 1
        self.assertEqual(
            User.objects.count(),
            users_count,
            'Количество пользователей не увеличилось.')

    def test_two_equal_user_are_impossible(self):
        """Проверяем, что нельзя создать двух одинаковых пользователей"""
        users_count = User.objects.count()
        forms_dates = {
            'username': 'Vinni Stuh',
            'email': 'Vinni@stuh.ru',
            'password1': '123456789qw',
            'password2': '123456789qw',
        }

        response = self.guest_client.post(
            reverse('users:signup'),
            data=forms_dates,
            follow=True
        )
        # Проверяем, изменилось ли количество пользователей
        self.assertEqual(
            User.objects.count(),
            users_count,
            'Количество пользователей увеличилось.'
        )

        # Проверим, что ничего не упало
        self.assertEqual(
            response.status_code,
            HTTPStatus.OK,
            'Все упало шеф.'
        )
