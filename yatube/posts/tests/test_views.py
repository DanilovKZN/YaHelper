from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.cache import caches
from django.core.files.uploadedfile import SimpleUploadedFile
from django import forms
from django.test import TestCase, Client
from django.urls import reverse

from ..models import Post, Group, Comment, Follow


User = get_user_model()


# Подготовка обьектов
class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
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
        cls.user_author = User.objects.create_user(username='Mr.tester')
        cls.user_new_author = User.objects.create_user(username='Pypkin')
        cls.test_user = User.objects.create_user(username='Yunga')
        cls.group = Group.objects.create(
            title='TestName',
            description='TestDescription',
            slug='TestSlug'
        )
        cls.group_second = Group.objects.create(
            title='Testiki',
            description='Kill me pleace',
            slug='Testiki-slug'
        )
        cls.post = Post.objects.create(
            text='Testing text: Slomay menya za moi english',
            author=cls.user_author,
            group=cls.group,
            image=cls.uploaded
        )
        cls.post_second = Post.objects.create(
            text='Testers',
            author=cls.user_author,
            group=cls.group_second,
            image=cls.uploaded
        )
        cls.comment = Comment.objects.create(
            post=cls.post,
            author=cls.user_author,
            text='My first comment'
        )
        cls.comment_second = Comment.objects.create(
            post=cls.post,
            author=cls.user_author,
            text='My second comment'
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user_author)
        self.second_authoriz_client = Client()
        self.second_authoriz_client.force_login(self.user_new_author)
        self.test_authorized_user = Client()
        self.test_authorized_user.force_login(self.test_user)

    # Проверяем, что адреса используют правильные шаблоны
    def test_uses_correct_templates_for_authirized(self):
        """ Проверяем соответсвие адресов и вызываемых
        шаблонов для авторизированного пользователя"""
        urls_templates = {
            reverse('posts:post_create'): 'posts/create_post.html',
            #reverse('posts:index'): 'posts/index.html',
            reverse(
                'posts:group_list',
                kwargs={'slug': self.group.slug}
            ): 'posts/group_list.html',
            reverse(
                'posts:profile',
                kwargs={'username': self.user_author.username}
            ): 'posts/profile.html',
            reverse(
                'posts:post_detail',
                kwargs={'post_id': self.post.pk}
            ): 'posts/post_detail.html',
            reverse(
                'posts:post_edit',
                kwargs={'post_id': self.post.pk}
            ): 'posts/create_post.html',
            reverse(
                'posts:post_delete',
                kwargs={'post_id': self.post.pk}
            ): 'posts/post_delete.html',
        }
        for reverse_name, template in urls_templates.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(
                    response,
                    template,
                    'Адрес не сходится с шаблоном'
                )

    def test_uses_correct_templates_for_not_authorized(self):
        """ Проверяем соответсвие адресов и вызываемых
        шаблонов для неавторизированного пользователя"""
        urls_templates = {
            reverse('posts:index'): 'posts/index.html',
            reverse(
                'posts:group_list',
                kwargs={'slug': self.group.slug}
            ): 'posts/group_list.html',
            reverse(
                'posts:profile',
                kwargs={'username': self.user_author.username}
            ): 'posts/profile.html',
            reverse(
                'posts:post_detail',
                kwargs={'post_id': self.post.pk}
            ): 'posts/post_detail.html',
        }
        for reverse_name, template in urls_templates.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.guest_client.get(reverse_name)
                self.assertTemplateUsed(
                    response,
                    template,
                    'Адрес не сходится с шаблоном'
                )

    # Проверяем содержимое контекстов
    def test_correct_context_page_obj(self):
        """Проверяем , что содержимое context совпадает с ожидаемым.
        Последний пост является первым в объекте пагинатора.
        Обход идет по index, group_posts, profile."""
        urls_for_testing = [
            #reverse('posts:index'),
            reverse(
                'posts:group_list',
                kwargs={'slug': self.group_second.slug}
            ),
            reverse(
                'posts:profile',
                kwargs={
                    'username':
                    self.post.author.username}
            )
        ]
        for value in urls_for_testing:
            with self.subTest(value=value):
                response = self.authorized_client.get(value)
                test_objects = response.context['page_obj'][0]
                self.assertEqual(
                    test_objects.text,
                    self.post_second.text,
                    'Тексты постов не равны.'
                )
                self.assertEqual(
                    test_objects.author,
                    self.post.author,
                    'Авторы не равны.'
                )
                self.assertEqual(
                    test_objects.pub_date,
                    self.post_second.pub_date,
                    'Даты публикаций не равны.'
                )
                if test_objects.group:
                    self.assertEqual(
                        test_objects.group,
                        self.post_second.group,
                        'Группы постов не равны.'
                    )
                if test_objects.image:
                    self.assertEqual(
                        test_objects.image,
                        self.post_second.image,
                        'Изображения разные.'
                    )

    def test_correct_context_text(self):
        """Проверяем , что содержимое context совпадает с ожидаемым.
        Последний пост является первым в объекте пагинатора.
        Обход идет по post_detail."""
        response = self.authorized_client.get(
            reverse(
                'posts:post_detail',
                kwargs={'post_id': self.post.pk})
        )
        test_object = response.context['text']
        self.assertEqual(
            test_object.text,
            self.post.text,
            'Тексты постов не равны.'
        )
        self.assertEqual(
            test_object.author,
            self.post.author,
            'Авторы не равны.'
        )
        self.assertEqual(
            test_object.pub_date,
            self.post.pub_date,
            'Даты публикаций не равны.'
        )
        if test_object.group:
            self.assertEqual(
                test_object.group,
                self.post.group,
                'Группы постов не равны.'
            )
        if test_object.image:
            self.assertEqual(
                test_object.image,
                self.post.image,
                'Изображения разные.'
            )

    # Теперь проверяем create_post
    def test_post_create_get_correct_context(self):
        """Шаблон post_create сформирован с правильным типом контекста."""
        response = self.authorized_client.get(
            reverse('posts:post_create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
            'image': forms.fields.ImageField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(
                    form_field,
                    expected,
                    'Типы полей не сходятся'
                )

    # Проверяем, что созданый пост при наличии группы
    # есть в index, group_list и profile
    def test_new_post_is_present_in_index_group_profile(self):
        """Проверяем, что созданый пост при наличии группы
        есть в index, group_list и prоfile """
        if PostPagesTests.post.group:
            urls_for_testing = [
                reverse('posts:index'),
                reverse(
                    'posts:group_list',
                    kwargs={'slug': self.group.slug}),
                reverse(
                    'posts:profile',
                    kwargs={
                        'username':
                        self.post.author.username}),
            ]
            for url in urls_for_testing:
                response = self.authorized_client.get(url)
                if len(response.context['page_obj']) > 1:
                    test_post = self.post_second.text
                    test_group = self.post_second.group
                else:
                    test_post = self.post.text
                    test_group = self.post.group
                post = response.context['page_obj'][0]
                self.assertEqual(
                    post.text,
                    test_post,
                    f'{post.text} не сoвпадает c '
                    f'{test_post}')
                self.assertEqual(
                    post.author,
                    self.post.author,
                    f'{post.author} не сoвпадает c'
                    f'{self.post.author}')
                self.assertEqual(
                    post.group,
                    test_group,
                    f'{post.group} не сoвпадает c'
                    f'{test_group}')

        # Пост не создался во второй группе
    def test_f_post_not_in_sec_group(self):
        """Пост присутствует только в
        первой (указанной) группе."""
        response = self.authorized_client.get(
            reverse(
                'posts:group_list',
                kwargs={'slug': self.group_second.slug})
        )
        last_post = len(response.context['page_obj']) - 1
        post = response.context['page_obj'][last_post]
        self.assertNotEqual(
            post.text,
            self.post.text,
            f'{post.text}  сoвпадает c'
            f'{self.post.text}'
        )

    def test_count_post_in_sec_grp_hasnt_changed(self):
        """Количество постов во второй
        группе осталось равным 1."""
        response = self.client.get(
            reverse(
                'posts:group_list',
                kwargs={
                    'slug':
                    self.group_second.slug}))
        self.assertEqual(
            len(response.context['page_obj']),
            1,
            'На второй странице второй группы создалось несколько постов.'
        )

    # Теперь проверяем post_edit
    def test_post_edit_get_correct_context(self):
        """Шаблон post_edit сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse(
                'posts:post_edit',
                kwargs={'post_id': self.post.pk})
        )
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(
                    form_field,
                    expected,
                    'Типы полей не сходятся'
                )

    # Проверяем создается ли комментарий
    def test_create_comment(self):
        """Проверяем, появился ли на странице
        созданный комментарий."""
        urls_for_testing = [
            reverse(
                'posts:post_detail',
                kwargs={'post_id': self.post.pk})
        ]
        for url in urls_for_testing:
            response = self.authorized_client.get(url)
            if len(response.context['comments']) > 0:
                comment = response.context['comments'][0]
                self.assertEqual(
                    comment.text,
                    self.comment.text,
                    f'{comment.text} не сoвпадает c '
                    f'{self.comment.text}'
                )
                self.assertEqual(
                    comment.post,
                    self.comment.post,
                    f'{comment.post} не сoвпадает c '
                    f'{self.comment.post}'
                )
                self.assertEqual(
                    comment.author,
                    self.comment.author,
                    f'{comment.author} не сoвпадает c '
                    f'{self.comment.author}'
                )
        #  Колличество комментариев = 1
        self.assertEqual(
            len(response.context['comments']),
            2,
            'Комментариев либо нет, либо создалось больше'
        )

    # Проверяем удаляется ли комментарий
    def test_delete_comment(self):
        """Проверяем удаляется ли комментарий
        и тот ли это комментарий."""
        count_comment = Comment.objects.count()
        last_comment = Comment.objects.last()
        # Тот ли коммент
        self.assertEqual(
            last_comment,
            self.comment_second,
            'Содержимое комментариев не совпадает'
        )
        # Теперь удаляем и прорверяем количество
        last_comment.delete()
        self.assertEqual(
            count_comment - 1,
            Comment.objects.count(),
            'Количество комментариев не изменилось'
        )
        
    # Тестирование кеша
    def test_cache_index(self):
        """Проверяем работает ли кеш,
        удалением последнего поста и сверки контекста
        до принудительного очищения кеша.
        """
        cache_index = caches['index_page']
        response_old = self.authorized_client.get(
            reverse('posts:index')
        )
        content_before_delete = response_old.content
        Post.objects.first().delete()
        responce_new = self.authorized_client.get(
            reverse('posts:index')
        )
        content_after_delete = responce_new.content
        self.assertEqual(
            content_before_delete,
            content_after_delete,
            'Контент страницы изменился.'
        )
        # Теперь очищаем кеш
        cache_index.clear()
        responce_new_new = self.authorized_client.get(
            reverse('posts:index')
        )
        content_after_delete_cache = responce_new_new.content
        self.assertNotEqual(
            content_after_delete,
            content_after_delete_cache,
            'Контент страницы не изменился.'
        )

    # Тестирование подписки/отписки
    def test_follow_and_unfollow(self):
        """Проверяем работоспособность подписки 
        и отписки авторизированного пользователя."""
        # Подписка
        self.authorized_client.get(
            reverse(
                'posts:profile_follow',
                kwargs={
                    'username':self.user_new_author.username
                }
            )
        )
        follower = Follow.objects.filter(
            user=self.user_author,
            author=self.user_new_author
        ).exists()
        self.assertEqual(
            follower,
            True,
            'Подписка не удалась'
        )

        # Отписка
        follows_count = Follow.objects.count()
        self.authorized_client.get(
            reverse(
                'posts:profile_unfollow',
                kwargs={
                    'username':self.user_new_author.username
                }
            )
        )
        self.assertEqual(
            follows_count - 1,
            Follow.objects.count(),
            'Отписка не удалась'
        )

    # Тестирование наличия записи у кого нужно 
    # и отсутсвие у кого не нужно
    def test_create_post_in_follower_and_not_unfol(self):
        """Проверяем создается ли запись у подписчика и 
        отсутвует у неподписчика."""
        self.authorized_client.get(
            reverse(
                'posts:profile_follow',
                kwargs={
                    'username':self.user_new_author.username
                }
            )
        )
        new_post = Post.objects.create(
            text='Hello world!',
            group=self.group_second,
            author=self.user_new_author
        )
        response = self.authorized_client.get(
            reverse(
                'posts:follow_index'
            )
        )
        object = response.context['page_obj'][0]
        self.assertEqual(
            object.text,
            new_post.text,
            f'{object.text} не сoвпадает c '
            f'{new_post.text}'
        )
        # Отсутствует у неподписчика
        self.test_authorized_user.get(
            reverse(
                'posts:profile_follow',
                kwargs={
                    'username':self.user_author.username
                }
            )
        )
        response = self.test_authorized_user.get(
            reverse(
                'posts:follow_index'
            )
        )
        object = response.context['page_obj'][0]
        self.assertNotEqual(
            object.text,
            new_post.text,
            f'{object.text} сoвпадает c '
            f'{new_post.text}'
        )
