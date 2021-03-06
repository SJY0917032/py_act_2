from django.urls import path, re_path
from . import views

app_name = 'instagram'

urlpatterns = [
    path('', views.index, name='index'),
    path('post/new/', views.post_new, name="post_new"),
    path('post/<int:pk>/', views.post_detail, name="post_detail"),
    path('post/<int:pk>/like', views.post_like, name="post_like"),
    path('post/<int:pk>/dislike', views.post_dislike, name="post_dislike"),
    path('post/<int:post_pk>/comment/new', views.post_comment_new, name="comment_new"),
    re_path(r'^(?P<username>[\w.@+-]+)/$', views.user_page, name="user_page"),
]
