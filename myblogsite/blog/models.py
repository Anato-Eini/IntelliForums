from django.db import models
from django.contrib.auth.hashers import check_password

class User(models.Model):
    username = models.CharField(max_length=100)
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

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    published_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

class UserPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE)
    text = models.TextField()
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} on {self.post.title}"

