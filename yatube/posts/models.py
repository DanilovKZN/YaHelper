from django.contrib.auth import get_user_model
from django.db import models

from core.models import CreatedModel

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200, null=False, verbose_name='Группа')
    slug = models.SlugField(max_length=20, unique=True)
    description = models.TextField(verbose_name='Описание')

    def __str__(self) -> str:
        return self.title


class Post(CreatedModel, models.Model):
    text = models.TextField(
        verbose_name='Публикация',
        help_text='Наберите текст...'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор'
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Группа'
    )
    image = models.ImageField(
        'Изображение',
        upload_to='posts/',
        blank=True
    )

    class Meta:
        ordering = ["-pub_date"]
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self) -> str:
        return self.text
        # return self.text[:15]


class Comment(CreatedModel, models.Model):
    post = models.ForeignKey(
        Post,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментарий'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментарий'
    )
    text = models.TextField(
        verbose_name='Комментарий',
        help_text='Наберите текст...'
    )
    #image = models.ImageField(
    #     'Изображение',
    #     upload_to='comments/',
    #     blank=True
    # )
    
    def __str__(self) -> str:
        return self.text


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'], name='ban on signing')
        ]


class InfoUser(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_info'
    )
    first_name = models.CharField(
        max_length= 50,
        null= False,
        verbose_name='Имя',
        help_text='Введите имя.',
        default='Аноним'
    )
    last_name = models.CharField(
        max_length= 50,
        null= False,
        verbose_name='Фамилия',
        help_text='Введите фамилию.',
        default='Анонимов'
    )
    experience = models.CharField(
        max_length= 10,
        null= False,
        verbose_name='Стаж работы',
        help_text='Введите свой стаж.',
        default='0'
    )
    year_of_release = models.CharField(
        max_length= 10,
        null= False,
        verbose_name='Год выпуска',
        help_text='Введите год выпуска.',
        default='1812'
    )
    city = models.CharField(
        max_length= 10,
        null= False,
        verbose_name='Город проживания',
        help_text='Введите свой город.',
        default='Забугоровск'
    )
    kogorta = models.CharField(
        max_length= 30,
        null= False,
        verbose_name='Когорта',
        help_text='Введите свою когорту.',
        default='0'
    )
    image = models.ImageField(
        'Изображение',
        upload_to='user_profile/',
        blank=True
    )
    information = models.TextField(
        verbose_name='Краткая информация',
        default='Я просто посмотреть зашёл.'
    )


class SearchPost(models.Model):
    text = models.CharField(
        max_length= 50,
        verbose_name='Поиск',
        help_text='Введите что-нужно',
    )
