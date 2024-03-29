from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, InfoUserForm, PostForm, SearchPostForm
from .models import Comment, Follow, Group, InfoUser, Post, User

POSTS_IN_PAGE_FOR_PAGINATOR = 10


def paginator(request, post_list):
    """Пагинатор."""
    paginator = Paginator(post_list, POSTS_IN_PAGE_FOR_PAGINATOR)
    page_number = request.GET.get('page', 1)
    page_object = paginator.get_page(page_number)
    return page_object


def index(request):
    """Главная страница."""
    template = 'posts/index.html'
    post_list = Post.objects.all()
    page_object = paginator(request, post_list)
    context = {
        'page_obj': page_object,
    }
    return render(request, template, context)


def group_posts(request, slug):
    """Посты группы."""
    template = 'posts/group_list.html'
    groups = get_object_or_404(Group, slug=slug)
    post_list = groups.posts.all()
    page_object = paginator(request, post_list)
    context = {
        'posts': post_list,
        'group': groups,
        'page_obj': page_object,
    }
    return render(request, template, context)


def profile(request, username):
    """Личная страница."""
    names = []
    author = get_object_or_404(User, username=username)
    following = request.user.follower.all()
    for name in following:
        names.append(name.author.username)
    template = 'posts/profile.html'
    post_list = Post.objects.filter(author=author)
    page_object = paginator(request, post_list)
    posts_count = post_list.count()
    context = {
        'author': author,
        'posts_count': posts_count,
        'page_obj': page_object,
        'post_list': post_list,
        'following': names,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    """Страница поста."""
    text = get_object_or_404(Post, pk=post_id)
    form_com = CommentForm(request.POST or None)
    comments = text.comments.all()
    template = 'posts/post_detail.html'
    post_count = text.author.posts.count()
    comment_count = comments.count()
    context = {
        'text': text,
        'post_count': post_count,
        'form': form_com,
        'comments': comments,
        'com_count': comment_count,
    }
    return render(request, template, context)


@login_required
def create_post(request):
    """Создаем пост."""
    template = 'posts/create_post.html'
    success_url = 'posts:profile'
    form = PostForm(request.POST or None,
                    files=request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(success_url, post.author.username)
    return render(request, template, {'form': form})


@login_required
def post_edit(request, post_id):
    """Редактируем пост."""
    template = 'posts/create_post.html'
    success_url = 'posts:post_detail'
    unsuccess_url = 'posts:profile'
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect(unsuccess_url, post.author)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(success_url, post_id)
    return render(request, template, {'form': form})
    


@login_required
def delete_post(request, post_id):
    """Удаляем пост."""
    success_url = 'posts:profile'
    template = 'posts/post_delete.html'
    post = get_object_or_404(Post, pk=post_id)
    if post.author == request.user:
        if request.method == 'POST':
            post.delete()
            return redirect(success_url, request.user)
        return render(request, template, {'post': post})
    else:
        return redirect(success_url, post.author)


@login_required
def add_comment(request, post_id):
    """Добавляем комментарий к посту."""
    success_url = 'posts:post_detail'
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.filter(active=True)
    form = CommentForm(
        request.POST or None,
        files=request.FILES or None
    )
    if request.method == 'POST':
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect(success_url, post_id)
    return render(
        request,
        template,
        {
            'form': form,
            'comments': comments,
        }
    )


@login_required
def delete_comment(request, post_id, com_id):
    """Удаляем комментарий поста."""
    success_url = 'posts:post_detail'
    post = get_object_or_404(Post, pk=post_id)
    comment = get_object_or_404(Comment, pk=com_id)
    if request.method == 'POST':
        if (
            comment.author == request.user or post.author == request.user
        ):
            comment.delete()
            return redirect(success_url, post_id)


@login_required
def follow_index(request):
    """Посты пользователей, на которых мы подписаны."""
    posts = Post.objects.filter(
        author__following__user=request.user
    )
    page_object = paginator(request, posts)
    context = {
        'page_obj': page_object,
    }
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    """Подписываемся на пользователя."""
    post_author = get_object_or_404(
        User,
        username=username
    )
    if post_author != request.user:
        Follow.objects.get_or_create(
            user=request.user,
            author=post_author
        )
    return redirect('posts:profile', post_author.username)


@login_required
def profile_unfollow(request, username):
    """Отписываемся от пользователя."""
    good_bay_man = get_object_or_404(
        Follow.objects.filter(
            user=request.user,
            author__username=username
        )
    )
    good_bay_man.delete()
    return redirect('posts:profile', username)


def info_user(request, username):
    """Информация о пользователе."""
    template = 'posts/personal_page.html'
    user_pr = get_object_or_404(User, username=username)
    information = InfoUser.objects.filter(user=user_pr)
    context = {
        'information': information,
    }
    return render(request, template, context)


@login_required
def edit_info_user(request, username):
    """Редактирование информации о полдьзователе."""
    template = 'posts/personal_page_edit.html'
    success_url = 'posts:index'
    unsuccess_url = 'posts:index'
    user_pr = get_object_or_404(User, username=username)
    if user_pr == request.user:
        form = InfoUserForm(
            request.POST or None,
            files=request.FILES or None,
            instance=user_pr
        )
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                return redirect(success_url, username)
        return render(request, template, {'form': form})
    return redirect(unsuccess_url, username)


def search_post_info(request):
    """Ищем пост."""
    template = 'posts/search_post.html'
    form = SearchPostForm(request.POST or None)
    replace_buttom = False
    if request.method == 'POST':
        if form.is_valid():
            date = form.cleaned_data.get('text')
            result = Post.objects.filter(text__icontains=date)
            if not result:
                replace_buttom = True
            page_object = paginator(request, result)
            return render(
                request,
                template,
                {
                    'page_obj': page_object,
                    'replace_buttom': replace_buttom,
                }
            )
    return render(request, template, {'form': form})
