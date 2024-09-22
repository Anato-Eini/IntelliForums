from django.contrib import admin
from .models import *

class PostAdmin(admin.ModelAdmin):
    """
    forum_ref = models.ForeignKey(Forum, on_delete=models.CASCADE)
    user_ref = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    """
    list_display = (
        'id',
        'forum_ref',
        'user_ref',
        'title',
        'content',
        'created_at'
    )

class ForumAdmin(admin.ModelAdmin):
    """
    title = models.CharField(max_length=100)
    description = models.TextField()
    """
    list_display = (
        'id',
        'title',
        'description'
    )

class CommentAdmin(admin.ModelAdmin):
    """
    user_post_ref = models.ForeignKey(UserPost, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    """
    list_display = (
        'id',
        'user_post_ref',
        'content',
        'created_at',
        'image',
        'user_ref'
    )

class UserAdmin(admin.ModelAdmin):
    """
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField()
    birth_date = models.DateField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user_type = models.IntegerField() #Admin = 0, user = 1
    """
    list_display = (
        'id',
        'username',
        'password',
        'email',
        'birth_date',
        'first_name',
        'last_name',
        'user_type'
    )

class UserPostAdmin(admin.ModelAdmin):
    """
    post_ref = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_ref = models.ForeignKey(User, on_delete=models.CASCADE)
    """
    list_display = (
        'id',
        'post_ref',
        'user_ref'
    )

class VoteAdmin(admin.ModelAdmin):
    """
    user_ref = models.ForeignKey(User, on_delete=models.CASCADE)
    post_ref = models.ForeignKey(Post, on_delete=models.CASCADE)
    is_upvote = models.BooleanField()
    """
    list_display = (
        'id',
        'user_post_ref',
        'is_upvote'
    )

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Forum, ForumAdmin)
admin.site.register(UserPost, UserPostAdmin)
admin.site.register(Vote, VoteAdmin)