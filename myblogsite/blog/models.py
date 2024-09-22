import os
import shutil

from django.db import models
from django.contrib.auth.hashers import check_password, make_password

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField()
    birth_date = models.DateField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user_type = models.IntegerField(default=1)#Admin = 0, user = 1

    def __str__(self):
        return self.username

    def set_password(self, password):
        self.password = make_password(password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

class Forum(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()


def upload_path(instance, filename):
    return f"temporary/{filename}"

class Post(models.Model):
    forum_ref = models.ForeignKey(Forum, on_delete=models.CASCADE)
    user_ref = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to=upload_path, blank=True, null=True)

    def save(self, *args, **kwargs):
        change_path(self, "posts", args, kwargs)
        super().save(update_fields=['image'])

    def save_model(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

def change_path(model, folder, *args, **kwargs):
    model.save_model(*args, **kwargs)

    if model.image:
        old_path = model.image.path
        new_dir = f"media/{folder}/{model.id}/"
        base_name = os.path.basename(model.image.name)
        new_path = os.path.join(new_dir, base_name)

        if not os.path.exists(new_dir):
            os.makedirs(new_dir)

        shutil.move(old_path, new_path)

        model.image.name = f"{folder}/{model.id}/{base_name}"

class UserPost(models.Model):
    post_ref = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_ref = models.ForeignKey(User, on_delete=models.CASCADE)

class Vote(models.Model):
    user_post_ref = models.ForeignKey(UserPost, on_delete=models.CASCADE)
    is_upvote = models.BooleanField()

class Comment(models.Model):
    user_post_ref = models.ForeignKey(UserPost, on_delete=models.CASCADE)
    user_ref = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to=upload_path, blank=True, null=True)

    def save(self, *args, **kwargs):
        change_path(self, "comments", args, kwargs)
        super().save(update_fields=['image'])

    def save_model(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user_ref.username} on {self.user_post_ref.post_ref.title}"
