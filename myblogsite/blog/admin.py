from django.contrib import admin
from .models import *

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(User)
admin.site.register(Forum)
admin.site.register(UserPost)
admin.site.register(Vote)