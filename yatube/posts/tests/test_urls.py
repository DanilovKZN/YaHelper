from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from ..models import Post, Group

from http import HTTPStatus

User = get_user_model()


# Подготовка обьектов
class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user_author = User.objects.create_user(username='Mr.tester')
        cls.user_not_author = User.objects.create_user(username='Prohodimec')
        cls.group = Group.objects.create(
            title='TestName',
            description='TestDescription',
            slug='TestSlug'
        )
        cls.post = Post.objects.create(
            text='Testing text: Slomay menya za moi english',
            author=cls.user_author,
            group=cls.group,
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user_author)
        self.authoriz_not_author = Client()
        self.authoriz_not_author.force_login(self.user_not_author)

    # Проверяем сначала общедоступные страницы
    def test_url_for_everyone(self):
        """Проверка доступности адресов страниц
        открытых любому пользователю."""
        url_test_for_everyone = [
            f'/group/{self.group.slug}/',
            f'/posts/{self.post.pk}/',
            f'/profile/{self.user_author.username}/'
        ]

        for url in url_test_for_everyone:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(
                    response.status_code,
                    HTTPStatus.OK,
                    f'Ненайден адрес:{url}')

                # Проверяем страницы для авторизированного автора
    def test_url_for_authorized_users(self):
        """Проверка доступности адресов страниц открытых
        только авторизированному пользователю."""
        url_adress_for_authorized = [
            f'/posts/{self.post.pk}/edit/',
            f'/posts/{self.post.pk}/delete/',
            '/create/'
        ]
        for url in url_adress_for_authorized:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(
                    response.status_code,
                    HTTPStatus.OK,
                    f'Ненайден адрес:{url}'
                )

        # Теперь перевод на другую страницу,
        # если пользователь не авторизированный
    def test_urls_closed_for_prohodimec(self):
        """ Перенаправляем анонимного пользователя
        на страницу авторизации. """
        urls_closed = [
            '/create/',
            f'/posts/{self.post.pk}/edit/',
            f'/posts/{self.post.pk}/delete/',
            f'/posts/{self.post.pk}/comment/'
        ]
        for url in urls_closed:
            with self.subTest(url=url):
                response = self.guest_client.get(url, follow=True)
                addr_to_redir = f'/auth/login/?next={url}'
                self.assertRedirects(
                    response,
                    addr_to_redir
                )

    # Теперь перенаправляем авториз. пользователя
    # на главную страницу если он не автор
    def test_urls_closed_for_not_author(self):
        """ Перенаправляем авторизованного пользователя
        если он не автор поста."""
        urls_closed = [
            f'/posts/{self.post.pk}/edit/',
            f'/posts/{self.post.pk}/delete/',
        ]
        for url in urls_closed:
            with self.subTest(url=url):
                response = self.authoriz_not_author.get(
                    url,
                    follow=True
                )
                addr_to_redir = f'/profile/{self.post.author}/'
                self.assertRedirects(
                    response,
                    addr_to_redir
                )

    # Теперь прогоняем шаблоны автора-авторизованного,
    # а затем не автора-авторизованного

    def test_open_template_for_authorized_user_author(self):
        """ Отдаем авторизованному пользователю-автору шаблоны по адресам.
        Затем авторизированному, но не автору."""
        list_with_url_templates = [
            (f'/posts/{self.post.pk}/edit/',
                'posts/create_post.html'),
            (f'/posts/{self.post.pk}/delete/',
                'posts/post_delete.html'),
            ('/', 'posts/index.html'),
            (f'/group/{self.group.slug}/',
                'posts/group_list.html'),
            (f'/profile/{self.user_author.username}/',
                'posts/profile.html'),
            (f'/posts/{self.post.pk}/',
                'posts/post_detail.html'),
            ('/create/', 'posts/create_post.html')
        ]
        for url, template in list_with_url_templates:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(
                    response,
                    template,
                    'Адрес не сходится с шаблоном'
                )
        # Отдаем авторизованному пользователю
        # <но не автору> шаблоны по адресам.
        closed_list_with_url_templates = [
            '/create/',
            f'/posts/{self.post.pk}/edit/',
            f'/posts/{self.post.pk}/delete/'
        ]
        for url, template in list_with_url_templates:
            with self.subTest(url=url):
                if url not in closed_list_with_url_templates:
                    response = self.authoriz_not_author.get(url)
                    self.assertTemplateUsed(
                        response,
                        template,
                        'Адрес не сходится с шаблоном'
                    )

    # Теперь всем проходимцам
    def test_open_tamplate_for_everyone(self):
        """ Отдаем неавторизованному пользователю шаблоны по адресам."""
        dict_with_necessary_dates = {
            '/': 'posts/index.html',
            f'/group/{self.group.slug}/':
            'posts/group_list.html',
            f'/profile/{self.user_author.username}/':
            'posts/profile.html',
            f'/posts/{self.post.pk}/':
            'posts/post_detail.html',
            '/unexting_page/': '',
        }
        for url, arg in dict_with_necessary_dates.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                if arg:
                    self.assertTemplateUsed(
                        response,
                        arg,
                        'Адрес не сходится с шаблоном'
                    )
                else:
                    self.assertEqual(
                        response.status_code,
                        HTTPStatus.NOT_FOUND,
                        'Пришел другой статус'
                    )
