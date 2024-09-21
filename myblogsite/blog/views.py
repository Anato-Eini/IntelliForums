from django.contrib.auth import login, authenticate
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Post, Comment, User, UserPost
from .forms import *

def fetch_posts(request, pk, page_number):
    """
    Fetch posts
    if forum does exist, it will fetch appropriate posts else it will fetch all posts from all forums
    with 20 results per page
    """
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'home.html', {
        'posts' : _get_page_object(
            Paginator(
                UserPost.objects.select_related('post_ref')
                .filter(post_ref__forum_ref__id=pk)
                .values(
                    'post_ref__user_ref__username',
                    'post_ref__title',
                    'post_ref__content',
                    'post_ref__created_at'
                )
                if Forum.objects.filter(id=pk).exists() else UserPost.objects.select_related('post_ref')
                .values(
                    'post_ref__user_ref__username',
                    'post_ref__title',
                    'post_ref__content',
                    'post_ref__created_at'
                ),20
            ), page_number
        ).object_list,
        'page_number' : page_number,
        'forum_pk' : pk
    })

def _get_page_object(paginator_object, page_number):
    try:
        page_object = paginator_object.page(page_number)
    except PageNotAnInteger:
        page_object = paginator_object.page(1)
    except EmptyPage:
        page_object = paginator_object.page(paginator_object.num_pages)

    return page_object

def render_new_post(request, forum_pk):
    """Render general post form is forum_pk does exist else it will render a post particular to that forum"""
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        post = GeneralPostForm(request.POST, request.FILES) \
            if not Forum.objects.filter(id=forum_pk).exists() \
            else PostForm(request.POST, request.FILES)
        if post.is_valid():
            post.save()
    else:
        post = GeneralPostForm() \
            if not Forum.objects.filter(id=forum_pk).exists() \
            else PostForm()

    return render(request, 'post_form.html', {'form' : post})

def post_detail(request, pk):
    """Render a particular post"""
    if not request.user.is_authenticated:
        return redirect('login')

    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post)
    return render(request, 'post_detail.html', {'post': post, 'comments': comments})

@csrf_protect
def render_register(request):
    """Render a form for register page"""

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            if User.objects.filter(username=username).exists():
                form.add_error('username', 'Username already taken')
            else:
                user = User(
                    username=username,
                    first_name=form.cleaned_data.get('first_name'),
                    last_name=form.cleaned_data.get('last_name'),
                    email=form.cleaned_data.get('email'),
                    birth_date=form.cleaned_data.get('birth_date')
                )
                user.set_password(password)
                user.save()
                return redirect('login')
        else:
            raise forms.ValidationError('Please enter valid data')
    else:
        form = RegisterForm()

    return render(request, 'register_form.html', {'form' : form})

@csrf_protect
def login_post(request):
    """Render a form for login page"""

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect(reverse('home', args=[0, 1]))
        else:
            raise forms.ValidationError('Please enter valid data')
    else:
        form = LoginForm()

    return render(request, 'login_form.html', context={'form': form})
