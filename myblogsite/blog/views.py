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

    posts = posts[::-1]

    return render(request, 'home.html', {
        'posts' : posts,
        'page_number' : page_number,
        'forum_pk' : pk,
        'form' : form,
        'search_form' : search_form,
        'user' : request.user,
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

def go_default_page(request):
    return redirect('home', pk=0, page_number=1)


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

def edit_comment(request, comment_id, user_post_id):
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
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()

    return redirect(reverse('post_detail', args=[user_post_id, 0]))

#UPDATE POST

def update_post(request,pk):
    if request.method == 'POST':
        user_post = get_object_or_404(UserPost, pk=pk)
        post = user_post.post_ref 
        if request.user != post.user_ref:
            return HttpResponseForbidden("You are not allowed to edit this post.")
        
        return render(request, 'update_post.html', {
            'user_post_pk': user_post.pk,
            'post': post,
        })

#title
def update_post_title(request, pk):
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

    return render(request,'update_post.html',{
        'user_post_pk' : user_post.pk,
        'post' : post,
    })

#content
def update_post_content(request, pk):

    #pk refers to UserPost PK
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

#DELETE POST
def delete_post(request, pk):
    #pk refers to UserPost PK
    user_post = get_object_or_404(UserPost, pk=pk)  
    post = user_post.post_ref  
    if request.user != post.user_ref:
        return HttpResponseForbidden("You are not allowed to delete this post.")

    if request.method == 'POST':
        user_post.delete()
        post.delete()
        return redirect('home', pk=0, page_number=1)

    return redirect('home', pk=0, page_number=1) #redirect to home with default forum, adjust later


def add_favorite(request, post_id):
    
    pass