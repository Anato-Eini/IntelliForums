from django.conf.urls.static import static
from django.urls import path

from myblogsite import settings
from . import views

urlpatterns = [
    path('', views.login_post, name='login'),
    path('register/', views.render_register, name='register'),
    path('new_post/<int:forum_pk>/', views.render_new_post, name='new_post'),
    path('home/<int:pk>/<int:page_number>/', views.fetch_posts,name='home'),
    path('home/<int:pk>/<int:page_number>/', views.fetch_posts, name='posts_forum'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

