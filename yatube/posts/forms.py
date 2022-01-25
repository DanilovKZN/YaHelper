from django import forms
from django.forms import ModelForm

from .models import Comment, InfoUser, Post, SearchPost


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')
        labels = {
            'text': 'Текст',
            'group': 'Группа',
        }
        help_texts = {
            'text': 'Текст поста',
            'group': 'Группа к которой относится пост ',
        }
        error_messages = {
            'text': {'required': 'Тестовое поле не должно быть пустым!'},
        }

    def clean_text(self):
        value = self.cleaned_data['text']
        if not value:
            raise forms.ValidationError(
                'Поле должено содержать хотя бы букву!'
            )
        return value


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        # fields = ('text', 'image') # Комментарии с картинками
        fields = ('text',)
        labels = {
            'text': 'Текст',
        }
        help_texts = {
            'text': 'Ваш комментарий',
        }
        error_messages = {
            'text': {'required': 'Комментарий не должно быть пустым!'},
        }


class InfoUserForm(ModelForm):
    class Meta:
        model = InfoUser
        fields = (
            'first_name',
            'last_name',
            'experience',
            'city',
            'kogorta',
            'information',
            'image'
        )


class SearchPostForm(ModelForm):
    class Meta:
        model = SearchPost
        fields = ('text',)
