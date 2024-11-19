import logging
from pyexpat.errors import messages

from django.http import JsonResponse, HttpResponseForbidden
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.db.models import Q

from .forms import *
from .views_classes import *

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
        form = SearchForm(request.POST)
        if form.is_valid():
            substring = form.cleaned_data['content']
            choice = form.cleaned_data['choices']
            posts = _get_page_object(
                Paginator(
                    get_filtered_posts(
                        UserPost.objects.filter(
                                (Q(post_ref__title__icontains=substring) | Q(post_ref__content__icontains=substring)) &
                                Q(is_deleted=False))
                            .filter(id__in=Tag.objects.filter(forum_ref__id=choice)).values(
                                'post_ref__id',
                                'post_ref__user_ref__username',
                                'post_ref__title',
                                'post_ref__content',
                                'post_ref__created_at',
                                'post_ref__user_ref__picture',
                                'id'),
                            )
                    if Forum.objects.filter(id=choice).exists()
                    else get_filtered_posts(
                        UserPost.objects.filter(
                            Q(post_ref__title__icontains=substring) | 
                            Q(post_ref__content__icontains=substring) & 
                            Q(is_deleted=False)
                        )
                    ), 
                    20
                ), 
                page_number
            ).object_list
    else:
        posts = _get_page_object(
            Paginator(
                get_filtered_posts(
                    UserPost.objects.filter(
                        id__in=Tag.objects.filter(forum_ref__id=pk)
                    )
                )

                if Forum.objects.filter(id=pk).exists()
                else get_filtered_posts(UserPost.objects.select_related('post_ref').filter(is_deleted = False))
                , 20
            ), page_number
        ).object_list

    search_form = SearchForm()
    posts = posts[::-1]
    forums = Forum.objects.all()
    
    return render(request, 'home.html', {
        'posts' : posts,
        'page_number' : page_number,
        'forum_pk' : pk,
        'search_form' : search_form,
        'user' : request.user,
        'forums' : forums
    })

def get_filtered_posts(_object):
    return _object.values(
        'post_ref__id',
        'post_ref__user_ref__username',
        'post_ref__title',
        'post_ref__content',
        'post_ref__created_at',
        'post_ref__user_ref__picture',
        'id'
    )

def _get_page_object(paginator_object, page_number):
    """
    Pagination of object given a page number

    Parameters:
        paginator_object (paginator): Object to be paginated
        page_number (int): page number

    Returns:
        Page: paged object
    """

    try:
        page_object = paginator_object.page(page_number)
    except PageNotAnInteger:
        page_object = paginator_object.page(1)
    except EmptyPage:
        page_object = paginator_object.page(paginator_object.num_pages)

    return page_object

@csrf_protect
@login_required(login_url='login')
def new_post_form(request, forum_pk):
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
                # post.forum_ref = get_object_or_404(Forum, id=form.cleaned_data['choices'][0])

            else:
                raise ValidationError("Incorrect data")

        user_instance = User.objects.get(id=request.user.id)
        post.user_ref = user_instance
        post.save()
        # TODO store in a variable for line 169
        UserPost.objects.create(
            post_ref=post,
            user_ref=user_instance
        )

        # TODO USE TRANSACTION instead for loop
        for choice in form.cleaned_data['choices']:
            Tag.objects.create(
                user_post_ref=UserPost.objects.get(post_ref=post),
                forum_ref=Forum.objects.get(
                    id=choice
                )
            )

        return redirect(reverse('home', args=[0, 1]))
    else:
        form = GeneralPostForm() \
            if not Forum.objects.filter(id=forum_pk).exists() \
            else PostForm()

    return render(request, 'post_form.html', {'form': form})

@login_required(login_url='login')
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

    handle_view_post(request.user.id, int(pk))

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
                    'user_ref__id',
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
        'user' : request.user,

    })

def handle_view_post(user_pk, user_post_id):
    """
    Handles query of user viewing a post.
    If user haven't viewed post A, then this will insert a new row
    indicating that the user has already viewed post A

    Parameters:
        user_pk (int): User id
        user_post_id (int): UserPost id

    Returns:
        None
    """

    query = PostView.objects.filter(user_ref__id=user_pk, user_post_ref__id=user_post_id)

    if not query.exists():
        user_ref = get_object_or_404(User, id=user_pk)
        user_post_ref = get_object_or_404(UserPost, id=user_post_id)
        PostView.objects.create(
            user_ref=user_ref,
            user_post_ref=user_post_ref
        ).save()



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
    user_posts = UserPost.objects.filter(user_ref__id=request.user.id, is_deleted=False) #use userpost table para ma filter ang isDeleted
    deleted_user_posts = UserPost.objects.filter(user_ref__id=request.user.id, is_deleted=True)
    user_comments = Comment.objects.filter(user_ref__id=request.user.id)
    user_favorites = FavoritePost.objects.filter(user_ref__id=request.user.id, user_post_ref__is_deleted=False)

    
    return render(request, 'profile.html', {
        'username' : user.username,
        'is_staff' : user.is_staff,
        'picture' : user.picture.url,
        'user_posts' : user_posts,
        'user_comments' : user_comments,
        'user_favorites' : user_favorites,
        'deleted_user_posts': deleted_user_posts,
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

def go_default_page(request):
    """
    Redirect to the home page
    Args:
        request:

    Returns:

    """
    return redirect('home', pk=0, page_number=1)

def edit_comment(request, comment_id, user_post_id):
    """
    Edits comments
    Args:
        request:
        comment_id:
        user_post_id:

    Returns:

    """
    comment = get_object_or_404(Comment, id=comment_id)
    form = CommentForm(instance=comment)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)

        if form.is_valid:
            form.save()
            return redirect(reverse('post_detail', args=[user_post_id, 1]))

    return render(request, 'edit_comment.html', {
        'form': form,
        'comment': comment,
        'user_post_id': user_post_id,
    })

def delete_comment(request, comment_id, user_post_id):
    """
    Deletes comments
    Args:
        request:
        comment_id: Comment id
        user_post_id: UserPost id

    Returns:

    """
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()

    return redirect(reverse('post_detail', args=[user_post_id, 0]))

def update_post(request, pk):
    """
    Renders a page for updating post
    Args:
        request:
        pk: UserPost pk

    Returns:

    """
    if request.method == 'POST':
        user_post = get_object_or_404(UserPost, pk=pk)
        post = user_post.post_ref
        if request.user != post.user_ref:
            return HttpResponseForbidden("You are not allowed to edit this post.")

        return render(request, 'update_post.html', {
            'user_post_pk': user_post.pk,
            'post': post,
        })

def update_post_title(request, pk):
    """
    Update post title
    Args:
        request:
        pk: UserPost pk

    Returns:

    """
    user_post = get_object_or_404(UserPost, pk=pk)
    post = user_post.post_ref

    if request.user != post.user_ref:
        return HttpResponseForbidden("You are not allowed to edit this post.")

    if request.method == 'POST':
        new_title = request.POST.get('new_title')
        if new_title:
            post.title = new_title
            post.save()
            return redirect('post_detail', pk=user_post.pk, page_number=1)

    return render(request, 'update_post.html', {
        'user_post_pk': user_post.pk,
        'post': post,
    })

def update_post_content(request, pk):
    """
    Update post's content
    Args:
        request:
        pk: UserPost pk

    Returns:

    """
    user_post = get_object_or_404(UserPost, pk=pk)
    post = user_post.post_ref

    if request.user != post.user_ref:
        return HttpResponseForbidden("You are not allowed to edit this post.")

    if request.method == 'POST':
        new_content = request.POST.get('new_content')
        if new_content:
            post.content = new_content
            post.save()
            return redirect('post_detail', pk=user_post.pk, page_number=1)

    return redirect('post_detail', pk=user_post.pk, page_number=1)

def delete_post(request, pk):
    """
    Deletes post
    Args:
        request:
        pk: UserPost pk

    Returns:
        HttpResponseRedirect:

    """
    user_post = get_object_or_404(UserPost, pk=pk)
    post = user_post.post_ref
    if request.user != post.user_ref:
        return HttpResponseForbidden("You are not allowed to delete this post.")

    if request.method == 'POST':
        user_post.is_deleted = True  # Set is_deleted to True instead of deleting
        user_post.save()
        return redirect('home', pk=0, page_number=1)

    return redirect('home', pk=0, page_number=1)  # redirect to home with default forum, adjust later

def perma_delete(request, pk):
    """
    Permanent deletion of a post
    Args:
        request:
        pk:

    Returns:
        HttpResponseRedirect:

    """
    user_post = get_object_or_404(UserPost, pk=pk)
    post = user_post.post_ref
    post.delete()

    return redirect('profile')


def add_favorite(request, post_id):
    """
    Adds a post to favorites
    Args:
        request:
        post_id: Post id

    Returns:
        HttpResponseRedirect:

    """
    favorite_object = FavoritePost.objects.filter(user_post_ref__id=post_id, user_ref__id=request.user.id).first()
    if favorite_object:
        favorite_object.delete()
    else:
        FavoritePost.objects.create(
            user_post_ref=UserPost.objects.get(pk=post_id),
            user_ref=User.objects.get(id=request.user.id),
        )

    return redirect(reverse('post_detail', args=[post_id, 0]))


@csrf_protect



def restore_post(request, pk):
    """
    Restores a post
    Args:
        request:
        pk: UserPost pk

    Returns:

    """
    user_post = get_object_or_404(UserPost, pk=pk)
    user_post.is_deleted = False
    user_post.save()
    return redirect('profile')


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

def num_view(request):
    """
    Fetch view count of a particular post

    Parameters:
        request (HttpRequest): request object

    Ajax Parameters:
        pk (int): UserPost id

    Returns:
        JsonResponse: returns a JsonResponse number of views of a particular post
    """

    pk = request.GET.get('pk')
    return JsonResponse({
        'view_count' : PostView.objects.filter(user_post_ref__id=pk).count(),
    })

def num_comments(request):
    """
    Fetch comment count of a particular post

    Parameters:
        request (HttpRequest): request object

    Ajax Parameters:
        pk (int): UserPost id

    Returns:
        JsonResponse: returns a JsonResponse number of comments of a particular post
    """

    pk = request.GET.get('pk')
    return JsonResponse({
        'comment_count' : Comment.objects.filter(user_post_ref__id=pk).count(),
    })

