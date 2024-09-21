from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Post, Comment, User, Forum, UserPost
from .forms import *

def fetch_posts_forum(request, pk, page_number):
    return render(request, 'post_list.html', {
        'posts' : _get_page_object(
            Paginator(
                UserPost.objects.select_related('post_ref')
                .filter(post_ref__forum_ref__id=pk)
                .values(
                    'post_ref__user_ref__username',
                    'post_ref__title',
                    'post_ref__content',
                    'post_ref__created_at'
                ), 20), page_number).object_list
    })

def _get_page_object(paginator_object, page_number):
    try:
        page_object = paginator_object.page(page_number)
    except PageNotAnInteger:
        page_object = paginator_object.page(1)
    except EmptyPage:
        page_object = paginator_object.page(paginator_object.num_pages)

    return page_object

def fetch_posts(request, page_number):
    return render(request, 'post_list.html', {
        'posts': _get_page_object(Paginator(UserPost.objects.select_related('post_ref')
        .values(
            'post_ref__user_ref__username',
            'post_ref__title',
            'post_ref__content',
            'post_ref__created_at'
        ), 20), page_number).object_list
    })

def get_forums(request):
    return render(request, 'forum.html', {'forums': Forum.objects.all()})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post)
    return render(request, 'post_detail.html', {'post': post, 'comments': comments})

@csrf_protect
def render_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            birth_date = form.cleaned_data.get('birth_date')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')


            if User.objects.filter(username=username).exists():
                form.add_error('username', 'Username already taken')
            else:
               User(
                    username = username,
                    password = make_password(password),
                    email = email,
                    birth_date = birth_date,
                    first_name = first_name,
                    last_name = last_name,
                    user_type=1
               ).save()
               return redirect('login')
        else:
            raise forms.ValidationError('Please enter valid data')
    else:
        form = RegisterForm()

    return render(request, 'register_form.html', {'form' : form})

@csrf_protect
def login_post(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            try:
                user = User.objects.get(username=username)
                if not user.check_password(password):
                    form.add_error('password', 'Incorrect password')
                else:
                    request.session['pk'] = user.pk
                    return redirect('home')
            except User.DoesNotExist:
                form.add_error('username', 'Username does not exist')
        else:
            raise forms.ValidationError('Please enter valid data')
    else:
        form = LoginForm()

    return render(request, 'login_form.html', context={'form': form})

def post_new(request):
    pass