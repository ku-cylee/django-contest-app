from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_out/', views.sign_out, name='sign_out'),
    path('category/<int:category_id>/', views.category_view_head, name='category_view_head'),
    path('category/<int:category_id>/page/<int:page>', views.category_view, name='category_view'),
    path('category/create/', views.create_category, name='create_category'),
    path('category/delete/<int:category_id>/', views.delete_category, name='delete_category'),
    path('article/<int:article_id>/', views.get_article, name='get_article'),
    path('article/compose/<int:category_id>/', views.compose_article, name='compose_article'),
    path('article/edit/<int:article_id>/', views.edit_article, name='edit_article'),
    path('article/delete/<int:article_id>/', views.delete_article, name='delete_article'),
    path('comment/compose/<int:article_id>', views.compose_comment, name='compose_comment'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('like/<int:article_id>/', views.like, name='like'),
    path('profile/<str:username>/', views.profile_index, name='profile_index'),
    path('profile/<str:username>/articles/', views.profile_articles, name='profile_articles'),
]
