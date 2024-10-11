from pyexpat.errors import messages
from django.http import JsonResponse
import logging

from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.db.models import Q

from .forms import *

def go_default_page(request):
    return redirect('home', pk=0, page_number=1)

@csrf_protect
def fetch_posts(request, pk, page_number):
    """
    Fetch posts
    if forum does exist, it will fetch appropriate posts else it will fetch all posts from all forums
    with 20 results per page

    Parameters:
        request (HttpRequest): request object
        pk (int): forum primary key
        page_number (int): page number

    Returns:
        HttpResponse: HttpResponse object

    """
    posts = []
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'search_filter_form':
            form = SearchForm(request.POST)
            if form.is_valid():
                substring = form.cleaned_data['content']
                posts = _get_page_object(
                    Paginator(
                        get_filtered_posts(UserPost.objects.select_related('post_ref')
                        .filter(
                            (Q(post_ref__title__icontains=substring)) |
                                           Q(post_ref__content__icontains=substring)) & Q(post_ref__forum_ref__id=pk))
                        if Forum.objects.filter(id=pk).exists()
                        else get_filtered_posts(
                            UserPost.objects.select_related('post_ref')
                            .filter(Q(post_ref__title__icontains=substring) |
                                    Q(post_ref__content__icontains=substring))
                        ), 20
                    ), page_number
                ).object_list
        elif form_type == 'fetch_filter_forum':
            form = ForumForm(request.POST)
            if form.is_valid():
                return redirect('posts_forum', pk=form.cleaned_data.get('choices'), page_number=1)
    else:
        posts = _get_page_object(
            Paginator(
                get_filtered_posts(
                    UserPost.objects.select_related('post_ref').filter(post_ref__forum_ref__id=pk)
                )
                if Forum.objects.filter(id=pk).exists()
                else get_filtered_posts(UserPost.objects.select_related('post_ref'))
                ,20
            ), page_number
        ).object_list

    form = ForumForm()
    search_form = SearchForm()

    return render(request, 'home.html', {
        'posts' : posts,
        'page_number' : page_number,
        'forum_pk' : pk,
        'form' : form,
        'search_form' : search_form,
        'user' : request.user
    })

def get_filtered_posts(_object):
    return _object.values(
        'post_ref__id',
        'post_ref__user_ref__username',
        'post_ref__title',
        'post_ref__content',
        'post_ref__created_at',
        'id'
    )


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
    """
    Render general post form is forum_pk does exist else it will render a post particular to that forum

    Parameters:
        request (HttpRequest): request object
        forum_pk (int): Forum id

    Returns:
        HttpResponse: HttpResponse

    Raises:
        ValidationError: If form contains incorrect data

    """
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

def post_detail(request, pk, page_number):
    """
    Render a particular post, its votes and comments and their votes
    Receives primary key for user_post

    Parameters:
        request (HttpRequest): HttpRequest object
        pk (str) : UserPost id
        page_number (int) : Page number

    Returns:
        HttpResponse: Http response

    Raises:
        ValidationError: If form contains incorrect data
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
                    'id'
                ),
                20
            ),
            page_number
        ).object_list,
        "user_post_pk" : pk,
        'form' : form,
        'post_upvotes' : VotePost.objects.select_related('user_post')
                  .filter(user_post_ref__id=pk, is_upvote=True).count(),
        'post_downvotes' : VotePost.objects.select_related('user_post')
                  .filter(user_post_ref__id=pk, is_upvote=False).count(),
        'user' : request.user
    })

@login_required(login_url='login')
def render_profile(request):
    """
    Renders profile Page

    Parameters:
        request (HttpRequest): request object

    Returns:
        HttpResponse: Http response

    """
    user = User.objects.get(id=request.user.id)
    return render(request, 'profile.html', {
        'username' : user.username,
        'is_staff' : user.is_staff,
        'picture' : user.picture.url,
    })

@csrf_protect
def render_register(request):
    """
    Render a form for register page

    Parameter:
        request (HttpRequest): request object

    Returns:
        HttpResponse : Http response
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created!')
            return redirect('login')
        else:
            messages.error(request, 'Incorrect data')
    else:
        form = RegisterForm()

    return render(request, 'register_form.html', {'form' : form})


#AJAX REQUESTS--------------------------------------------------------------------------------------------------------

@login_required(login_url='login')
def post_vote(request):
    """
    Handles POST request for post's votes

    Parameters:
        request (HttpRequest): request object

    Returns:
        JsonResponse: key -> upvote, downvote
    """
    post_pk = int(request.POST.get('pk')) #UserPost id
    is_upvote = int(request.POST.get('type')) == 1
    vote_object = VotePost.objects.filter(user_post_ref__id=post_pk, user_ref__id=request.user.id).first()
    if vote_object:
        if vote_object.is_upvote == is_upvote:
            vote_object.delete()
        else:
            vote_object.is_upvote = is_upvote
            vote_object.save()
    else:
        VotePost.objects.create(
            user_post_ref=UserPost.objects.get(pk=post_pk),
            user_ref = User.objects.get(id=request.user.id),
            is_upvote = is_upvote
        )

    return JsonResponse({
        'upvote' : VotePost.objects.filter(user_post_ref__id=post_pk, is_upvote=True).count(),
        'downvote' : VotePost.objects.filter(user_post_ref__id=post_pk, is_upvote=False).count(),
    })

@login_required(login_url='login')
def comment_vote(request):
    """
    Handles POST | GET request for comment's votes

    Parameters:
        request (HttpRequest): request object

    Returns:
        JsonResponse: key -> upvote, downvote
    """
    if request.method == "POST":
        comment_ref_id = int(request.POST.get('pk'))  # Comment.id
        is_upvote = int(request.POST.get('type')) == 1  # 1-Upvote 2-Downvote
        vote_object = VoteComment.objects.filter(comment_ref__id=comment_ref_id, user_ref__id=request.user.id).first()
        if vote_object:
            if vote_object.is_upvote == is_upvote:
                vote_object.delete()
            else:
                vote_object.is_upvote = is_upvote
                vote_object.save()
        else:
            VoteComment.objects.create(
                comment_ref=Comment.objects.get(pk=comment_ref_id),
                user_ref=User.objects.get(id=request.user.id),
                is_upvote = is_upvote
            )
    else:
        comment_ref_id = int(request.GET.get('pk'))

    return JsonResponse({
        'upvote' : VoteComment.objects.filter(comment_ref__id=comment_ref_id, is_upvote=True).count(),
        'downvote' : VoteComment.objects.filter(comment_ref__id=comment_ref_id, is_upvote=False).count(),
    })

