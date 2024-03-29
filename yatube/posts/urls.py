from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.index, name='index'),
    path(
        'group/<slug:slug>/',
        views.group_posts,
        name='group_list'
    ),
    path(
        'profile/<str:username>/',
        views.profile,
        name='profile'
    ),
    path(
        'posts/<int:post_id>/',
        views.post_detail,
        name='post_detail'
    ),
    path(
        'create/',
        views.create_post,
        name='post_create'
    ),
    path(
        'posts/<int:post_id>/edit/',
        views.post_edit,
        name='post_edit'
    ),
    path(
        'posts/<int:post_id>/delete/',
        views.delete_post,
        name='post_delete'
    ),
    path(
        'posts/<int:post_id>/comment/',
        views.add_comment,
        name='add_comment'
    ),
    path(
        'posts/<int:post_id>/delete_comment/<int:com_id>/',
        views.delete_comment,
        name='delete_comment'
    ),
    path('follow/', views.follow_index, name='follow_index'),
    path(
        'profile/<str:username>/follow/',
        views.profile_follow,
        name='profile_follow'
    ),
    path(
        'profile/<str:username>/unfollow/',
        views.profile_unfollow,
        name='profile_unfollow'
    ),
    path(
        'info_user/<str:username>/',
        views.info_user,
        name='page_user'
    ),
    path(
        'info_user/<str:username>/edit/',
        views.edit_info_user,
        name='page_user_edit'
    ),
    path(
        'search/',
        views.search_post_info,
        name='search_post'
    ),
]
