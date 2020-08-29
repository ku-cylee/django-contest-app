import math

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .lib import *
from .forms import *
from .models import *


def index(req):
    return render(req, 'index.html', {
        'form': CategoryForm(),
        'categories': Category.objects.all().filter(is_deleted=False),
    })


def sign_up(req):
    if req.user.is_authenticated:
        return send_status(404)
    if req.method == 'GET':
        return sign_up_form(req)
    if req.method == 'POST':
        return sign_up_post(req)
    return send_status(404)


def sign_up_form(req):
    return render(req, 'auth/sign_up.html', {
        'form': SignUpForm(),
    })


def sign_up_post(req):
    form = SignUpForm(req.POST)
    if not form.is_valid():
        return send_status(400)
    
    user = User.objects.create_user(
        username=form.cleaned_data['username'],
        password=form.cleaned_data['password'],
        email=form.cleaned_data['email'],
    )
    user.save()
    return redirect('sign_in')


def sign_in(req):
    if req.user.is_authenticated:
        return send_status(404)
    if req.method == 'GET':
        return sign_in_form(req)
    if req.method == 'POST':
        return sign_in_post(req)
    return send_status(404)


def sign_in_form(req):
    return render(req, 'auth/sign_in.html', {
        'form': SignInForm(),
    })


def sign_in_post(req):
    form = SignInForm(req.POST)
    if not form.is_valid():
        return send_status(400)
    
    user = authenticate(
        username=form.cleaned_data['username'],
        password=form.cleaned_data['password'],
    )
    
    if user:
        login(req, user)
        return redirect('index')
    else:
        return send_status(401)


def sign_out(req):
    logout(req)
    return redirect('index')


def category_view_head(req, category_id):
    return redirect('category_view', category_id=category_id, page=1)


def category_view(req, category_id, page):
    category = get_object_or_404(Category, id=category_id, is_deleted=False)

    articles = Article.objects.all().filter(
        is_deleted=False, category=category).order_by('-id')

    COUNT = 5

    start_index = (page - 1) * COUNT
    end_index = page * COUNT

    page_count = math.ceil(len(articles) / COUNT)

    return render(req, 'articles/index.html', {
        'page': page,
        'category': category,
        'articles': articles[start_index:end_index],
        'has_prev': page > 1,
        'has_next': page < page_count,
    })


def create_category(req):
    if not req.user.is_authenticated:
        return send_status(404)
    if req.method != 'POST':
        return send_status(404)

    form = CategoryForm(req.POST)
    if not form.is_valid():
        return send_status(400)

    category = Category.objects.create(
        name=form.cleaned_data['name'],
        creator=req.user,
    )
    category.save()

    return redirect('category_view_head', category_id=category.id)


def delete_category(req, category_id):
    if not req.user.is_authenticated:
        return send_status(404)

    category = get_object_or_404(Category, id=category_id, creator=req.user, is_deleted=False)
    category.is_deleted = True
    category.save()

    return redirect('index')


def get_article(req, article_id):
    article = get_object_or_404(Article, id=article_id, is_deleted=False)
    comments = Comment.objects.filter(article=article, is_deleted=False)
    likes = Like.objects.filter(article=article)
    if req.user.is_authenticated:
        liked = likes.filter(user=req.user).count() > 0
    else:
        liked = False

    return render(req, 'articles/details.html', {
        'article': article,
        'comments': comments,
        'comments_count': comments.count(),
        'likes_count': likes.count(),
        'liked': liked,
        'form': CommentForm(),
    })


def compose_article(req, category_id):
    if not req.user.is_authenticated:
        return send_status(404)
    
    category = get_object_or_404(Category, id=category_id, is_deleted=False)

    if req.method == 'GET':
        return compose_article_form(req, category)
    if req.method == 'POST':
        return compose_article_post(req, category)
    return send_status(404)


def compose_article_form(req, category):
    return render(req, 'articles/compose.html', {
        'form': ArticleForm(),
        'is_compose': True,
    })


def compose_article_post(req, category):
    form = ArticleForm(req.POST)
    if not form.is_valid():
        return send_status(400)
    
    new_article = Article.objects.create(
        title=form.cleaned_data['title'],
        content=form.cleaned_data['content'],
        author=req.user,
        category=category,
    )
    new_article.save()

    return redirect('get_article', article_id=new_article.id)


def edit_article(req, article_id):
    if not req.user.is_authenticated:
        return send_status(404)
    
    article = get_object_or_404(Article, id=article_id, author=req.user, is_deleted=False)

    if req.method == 'GET':
        return edit_article_form(req, article)
    if req.method == 'POST':
        return edit_article_post(req, article)
    return send_status(404)


def edit_article_form(req, article):
    return render(req, 'articles/compose.html', {
        'form': ArticleForm(initial={
            'title': article.title,
            'content': article.content,
        }),
        'is_compose': False,
    })


def edit_article_post(req, article):
    form = ArticleForm(req.POST)
    if not form.is_valid():
        return send_status(400)

    article.title = form.cleaned_data['title']
    article.content = form.cleaned_data['content']
    article.save()

    return redirect('get_article', article_id=article.id)


def delete_article(req, article_id):
    if not req.user.is_authenticated:
        return send_status(404)
    
    article = get_object_or_404(Article, id=article_id, author=req.user, is_deleted=False)
    article.is_deleted = True
    article.save()

    return redirect('category_view_head', category_id=article.category.id)


def compose_comment(req, article_id):
    if req.method != 'POST' or not req.user.is_authenticated:
        return send_status(404)

    form = CommentForm(req.POST)
    if not form.is_valid():
        return send_status(400)
    
    article = get_object_or_404(Article, id=article_id, is_deleted=False)

    new_comment = Comment.objects.create(
        content=form.cleaned_data['content'],
        author=req.user,
        article=article,
    )
    new_comment.save()

    return redirect('get_article', article_id)


def delete_comment(req, comment_id):
    if not req.user.is_authenticated:
        return send_status(404)

    comment = get_object_or_404(Comment, id=comment_id, is_deleted=False, author=req.user)
    comment.is_deleted = True
    comment.save()

    return redirect('get_article', comment.article.id)


def like(req, article_id):
    if not req.user.is_authenticated:
        return send_status(404)

    article = get_object_or_404(Article, id=article_id, is_deleted=False)
    likes = Like.objects.all().filter(article=article, user=req.user)
    is_favor = likes.count() > 0
    
    if is_favor:
        likes[0].delete()
    else:
        Like.objects.create(article=article, user=req.user)
    return redirect('get_article', article_id=article_id)


def profile_index(req, username):
    user = get_object_or_404(User, username=username)
    return render(req, 'profile/index.html', {
        'profile_user': user,
    })


def profile_articles(req, username):
    user = get_object_or_404(User, username=username)
    articles = Article.objects.all().filter(author=user, is_deleted=False)

    return render(req, 'profile/articles.html', {
        'articles': articles,
        'profile_user': user,
    })
