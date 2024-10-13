from django.conf.urls.static import static
from django.urls import path

from myblogsite import settings
from . import views
from .views import CustomLoginView, CustomLogoutView

urlpatterns = [
    path('', views.go_default_page, name='default_page'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', views.render_register, name='register'),
    path('new_post/<int:forum_pk>/', views.new_post_form, name='new_post'),
    path('home/<int:pk>/<int:page_number>/', views.fetch_posts,name='home'),
    path('post_detail/<int:pk>/<int:page_number>/', views.post_detail, name='post_detail'),
    path('profile/', views.render_profile, name='profile'),
    path('login/', CustomLogoutView.as_view(next_page='login'), name='logout'),

    #AJAX
    path('post_vote/', views.post_vote, name='post_vote'),
    path('comment_vote/', views.comment_vote, name='comment_vote'),
    path('view_num/', views.num_view, name='fetch_view_num'),
    path('comment_num/', views.num_comments, name='fetch_comment_num'),
    path('post/<int:pk>/update_title/', views.update_post_title, name='update_post_title'), #UserPost pk
    path('post/<int:pk>/update_content/', views.update_post_content, name='update_post_content'), #UserPost pk
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),

    path('edit_comment/<int:comment_id>', views.edit_comment, name='edit_comment'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name="delete_comment")

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

