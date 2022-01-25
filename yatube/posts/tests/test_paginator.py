from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post
from ..views import POSTS_IN_PAGE_FOR_PAGINATOR

User = get_user_model()


class PaginatorViewsTest(TestCase):
    NOTES_IN_PAGE_PAGINTOR = 15
    NOTES_IN_SECOND_PAGE_PAG = (
        NOTES_IN_PAGE_PAGINTOR - POSTS_IN_PAGE_FOR_PAGINATOR
    )

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user_author_test = User.objects.create_user(username='Bad.tester')
        cls.group = Group.objects.create(
            title='TestName',
            description='TestDescription',
            slug='TestSlug')
        # Создаем посты в количестве NOTES_IN_PAGE_PAGINTOR
        testing_text = {}
        for key in range(PaginatorViewsTest.NOTES_IN_PAGE_PAGINTOR):
            testing_text['Apelsin' + '_' + str(key)] = (
                'This is text for testing paginator.')
        for key, var in testing_text.items():
            cls.key = Post.objects.create(
                text=var,
                author=cls.user_author_test,
                group=cls.group
            )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(
            self.user_author_test
        )

    def test_posts_in_first_and_second_pages(self):
        """Проверка: количество постов на первой
        и второй странице index, group_list, profile равно числу,
        указанному в POSTS_IN_PAGE_FOR_PAGINATOR и
        NOTES_IN_SECOND_PAGE_PAG.
        """
        url_expected_count = {
            reverse('posts:index'):
                POSTS_IN_PAGE_FOR_PAGINATOR,
            reverse(
                'posts:group_list',
                kwargs={'slug': self.group.slug}):
                POSTS_IN_PAGE_FOR_PAGINATOR,
            reverse(
                'posts:profile',
                kwargs={
                    'username':
                    self.user_author_test.username}):
                    POSTS_IN_PAGE_FOR_PAGINATOR,
            reverse('posts:index') + '?page=2':
                self.NOTES_IN_SECOND_PAGE_PAG,
            reverse(
                'posts:group_list',
                kwargs={'slug': self.group.slug}
            ) + '?page=2':
                self.NOTES_IN_SECOND_PAGE_PAG,
            reverse(
                'posts:profile',
                kwargs={
                    'username':
                    self.user_author_test.username
                }) + '?page=2':
                self.NOTES_IN_SECOND_PAGE_PAG,
        }
        for url, count in url_expected_count.items():
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(
                    len(response.context['page_obj']),
                    count,
                    'Количество записей не совпадает'
                )
