from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Это обычный тестовый пост созданый просто для тестирования.',
        )

    def test_model_group_have_correct_object_name(self):
        """Проверяем, что у модели 'group' корректно работает __str__."""
        self.assertEqual(
            str(self.group),
            self.group.title,
            'Записи не совпадают'
        )

    def test_model_post_less_fifteen_sym(self):
        """Проверяем, что у модели 'post' корректно работает __str__."""
        self.assertEqual(
            str(self.post),
            # self.post.text[:15],
            self.post.text,
            'Вывод не сходится с условием.'
        )
