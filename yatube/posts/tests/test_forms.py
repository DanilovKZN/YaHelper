import shutil
import tempfile

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from ..forms import PostForm
from ..models import Comment, Post, Group


User = get_user_model()
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=cls.small_gif,
            content_type='image/gif'
        )
        cls.user_author = User.objects.create_user(
            username='Mr.tester')
        cls.group_new = Group.objects.create(
            title='Samei_novii_group',
            description='samei-samei',
            slug='Novie_slug'
        )
        cls.form = PostForm()
        cls.post = Post.objects.create(
            text='Testing-testin-testi-test-tes-te-t',
            author=cls.user_author,
            group=cls.group_new
        )
        cls.comment = Comment.objects.create(
            post=cls.post,
            author=cls.user_author,
            text='My first comment!'
        )

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user_author)

    # Тестируем создание поста
    def test_create_post(self):
        """Заполняем форму и отправляем Post запрос,
        если форма валидна, то все Ок ."""
        posts_count = Post.objects.count()
        forms_dates = {
            'text': 'Welcome new text',
            'group': self.group_new.id,
            'image': self.uploaded,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=forms_dates,
            follow=True
        )

        # Осуществляется ли переход на страницу
        # пользователя, после создания поста
        self.assertRedirects(
            response,
            reverse(
                'posts:profile',
                kwargs={
                    'username':
                    self.user_author.username})
        )

        # Равен ли текст созданого поста
        # последнему в базе
        self.assertEqual(
            forms_dates['text'],
            Post.objects.first().text,
            'Тексты постов не равны.'
        )

        # Проверяем, изменилось ли количество постов
        posts_count += 1
        self.assertEqual(
            Post.objects.count(),
            posts_count,
            'Количество постов не увеличилось.'
        )

    # Тестируем редактирование поста
    def test_post_edit_and_new_context_in_post_detail(self):
        """Редактируем записи и отправляем Post запрос.
        Затем проверяем верно ли изменились данные и
        осуществился ли переход на страницу поста."""
        posts_count = Post.objects.count()
        forms_dates_for_edit = {
            'text': 'After edit only new, without testing-tes....',
            'group': self.group_new.id,
        }
        response = self.authorized_client.post(
            reverse(
                'posts:post_edit',
                kwargs={
                    'post_id':
                    self.post.id}),
            data=forms_dates_for_edit,
            follow=True
        )
        # Осуществляется ли переход на страницу
        # пользователя, после редактирования поста
        self.assertRedirects(
            response,
            reverse(
                'posts:post_detail',
                kwargs={
                    'post_id': self.post.id})
        )

        # Проверяем, неизменилось ли количество постов
        self.assertEqual(
            Post.objects.count(),
            posts_count,
            'Количество постов увеличилось.'
        )

        # А теперь проверяем, изменилось ли
        # содержание поста после редактирования
        obj = Post.objects.get(pk=self.post.pk)
        first_object = response.context['text']
        self.assertNotEqual(
            self.post.text,
            obj.text,
            'Записи равны.'
        )
        self.assertEqual(
            obj.author,
            self.post.author,
            f'{first_object.author} != '
            f'{self.post.author}'
        )
        self.assertEqual(
            obj.pub_date,
            self.post.pub_date,
            f'{first_object.pub_date} != '
            f'{self.post.pub_date}'
        )

        # Тестируем удаление поста

    def test_delete_post(self):
        """Проверяем удаляется ли пост и осуществлется
        переход на страницу пользователя."""
        posts_count = Post.objects.count()
        forms_dates_for_delete = {
            'text': self.post.text,
            'group': self.group_new.id,
        }
        response = self.authorized_client.post(
            reverse(
                'posts:post_delete',
                kwargs={'post_id': self.post.id}),
            forms_dates_for_delete,
            follow=True
        )
        # Осуществляется ли переход на страницу пользователя,
        # после создания поста
        self.assertRedirects(
            response,
            reverse(
                'posts:profile',
                kwargs={
                    'username':
                    self.post.author.username}
            )
        )

        # Проверяем, неизменилось ли количество постов
        self.assertEqual(
            Post.objects.count(),
            posts_count - 1,
            'Количество постов не уменьшилось.')
