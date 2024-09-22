from django.contrib.auth import login, authenticate
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .forms import *

@login_required(login_url='login')
def fetch_posts(request, pk, page_number):
    """
    Fetch posts
    if forum does exist, it will fetch appropriate posts else it will fetch all posts from all forums
    with 20 results per page
    """
    return render(request, 'home.html', {
        'posts' : _get_page_object(
            Paginator(
                UserPost.objects.select_related('post_ref')
                .filter(post_ref__forum_ref__id=pk)
                .values(
                    'post_ref__id',
                    'post_ref__user_ref__username',
                    'post_ref__title',
                    'post_ref__content',
                    'post_ref__created_at',
                    'id'
                )
                if Forum.objects.filter(id=pk).exists()
                else UserPost.objects.select_related('post_ref')
                .values(
                    'post_ref__id',
                    'post_ref__user_ref__username',
                    'post_ref__title',
                    'post_ref__content',
                    'post_ref__created_at',
                    'id'
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

@csrf_protect
@login_required(login_url='login')
def render_new_post(request, forum_pk):
    """Render general post form is forum_pk does exist else it will render a post particular to that forum"""
    if request.method == 'POST':
        if Forum.objects.filter(id=forum_pk).exists():
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.forum_ref = get_object_or_404(Forum, id=forum_pk)
            else:
                raise ValidationError("Incorrect data")
        else:
            form = GeneralPostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.forum_ref = get_object_or_404(Forum, id=form.cleaned_data['choices'])
            else:
                raise ValidationError("Incorrect data")

        user_instance = User.objects.get(id=request.user.id)
        post.user_ref = user_instance
        post.save()
        UserPost.objects.create(
            post_ref=post,
            user_ref=user_instance
        )
        return redirect(reverse('home', args=[0, 1]))
    else:
        form = GeneralPostForm() \
            if not Forum.objects.filter(id=forum_pk).exists() \
            else PostForm()

    return render(request, 'post_form.html', {'form' : form})

@login_required(login_url='login')
def post_detail(request, pk, page_number):
    """
    Render a particular post
    Receives primary key for user_post
    """
    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user_post_ref = get_object_or_404(UserPost, id=pk)
            comment.user_ref = get_object_or_404(User, id=request.user.id)
            page_number = 1
            comment.save()
        else:
            raise ValidationError("Incorrect data")
    else:
        form = CommentForm()

    return render(request, 'post_detail.html', {
        'post': get_object_or_404(Post, pk=UserPost.objects.get(pk=pk).post_ref.id),
        'comments': _get_page_object(
            Paginator(
                Comment.objects.select_related('user_ref')
                .filter(user_post_ref__id=pk)
                .values(
                    'content',
                    'created_at',
                    'image',
                    'user_ref__username',
                ),
                20
            ),
            page_number
        ).object_list,
        "user_post_pk" : pk,
        'form' : form,
        'upvotes' : _get_vote_number(True, pk),
        'downvotes' : _get_vote_number(False, pk)
    })

def _get_vote_number(upvote, user_post_pk):
    return (Vote.objects.select_related('user_post')
            .filter(user_post_ref__id=user_post_pk, is_upvote=upvote).count())

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
