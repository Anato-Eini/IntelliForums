from django.db import models
from django.contrib.auth.hashers import check_password

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField()
    birth_date = models.DateField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user_type = models.IntegerField() #Admin = 0, user = 1

    def __str__(self):
        return self.username

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

class Forum(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

class Post(models.Model):
    forum_ref = models.ForeignKey(Forum, on_delete=models.CASCADE)
    user_ref = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

class Vote(models.Model):
    user_ref = models.ForeignKey(User, on_delete=models.CASCADE)
    post_ref = models.ForeignKey(Post, on_delete=models.CASCADE)
    is_upvote = models.BooleanField()

class UserPost(models.Model):
    post_ref = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_ref = models.ForeignKey(User, on_delete=models.CASCADE)

class Comment(models.Model):
    user_post_ref = models.ForeignKey(UserPost, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} on {self.post.title}"

