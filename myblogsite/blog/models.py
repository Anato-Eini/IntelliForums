from datetime import date

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Users must have username')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField()
    birth_date = models.DateField(default=date.today)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    picture = models.ImageField(
        upload_to='profile/',
        default='profile/blank-profile-picture-973460_128012234212.png',
        blank=True,
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.username

class Forum(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

def upload_path(instance, filename):
    return f"{filename}"

class Post(models.Model):
    forum_ref = models.ForeignKey(Forum, on_delete=models.CASCADE)
    user_ref = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to=upload_path, blank=True, null=True)

    def __str__(self):
        return self.title

class UserPost(models.Model):
    post_ref = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_ref = models.ForeignKey(User, on_delete=models.CASCADE)

class VotePost(models.Model):
    user_post_ref = models.ForeignKey(UserPost, on_delete=models.CASCADE)
    user_ref = models.ForeignKey(User, on_delete=models.CASCADE)
    is_upvote = models.BooleanField()

class Comment(models.Model):
    user_post_ref = models.ForeignKey(UserPost, on_delete=models.CASCADE)
    user_ref = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to=upload_path, blank=True, null=True)

    def __str__(self):
        return f"{self.user_ref.username} on {self.user_post_ref.post_ref.title}"

class VoteComment(models.Model):
    comment_ref = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user_ref = models.ForeignKey(User, on_delete=models.CASCADE)
    is_upvote = models.BooleanField()
