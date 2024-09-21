from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_post, name='login'),
    path('register/', views.render_register, name='register'),
    path('home/<int', views.fetch_posts,name='home'),
    path('home/<int:pk>', views.fetch_posts_forum, name='posts_forum'),
    path('post/<int:pk>/', views.post_detail, name='post_detail')
]

