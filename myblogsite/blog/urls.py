from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path

from myblogsite import settings
from . import views

class CustomLoginView(LoginView):
    template_name = 'login_form.html'

urlpatterns = [
    path('', views.go_default_page, name='default_page'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', views.render_register, name='register'),
    path('new_post/<int:forum_pk>/', views.render_new_post, name='new_post'),
    path('home/<int:pk>/<int:page_number>/', views.fetch_posts,name='home'),
    path('forum/<int:pk>/<int:page_number>/', views.fetch_posts, name='posts_forum'),
    path('post_detail/<int:pk>/<int:page_number>/', views.post_detail, name='post_detail'),
    path('profile/', views.render_profile, name='profile'),
    path('login/', LogoutView.as_view(next_page='login'), name='logout'),


    #Ajax
    path('post_vote/', views.post_vote, name='post_vote'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

