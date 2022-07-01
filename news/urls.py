from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import BaseRegisterView, PostList, DeletePost, ChangePost, AddPost, upgrade_me, subscribe_me, unsubscribe_me
from .views import IndexView
from .views import PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = [
    path('login/',
         LoginView.as_view(template_name='news/login.html'),
         name='login'),
    path('logout/',
         LogoutView.as_view(template_name='news/logout.html'),
         name='logout'),
    path('signup/',
         BaseRegisterView.as_view(template_name='news/signup.html'),
         name='signup'),
    path('', IndexView.as_view()),
    path('<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('create/', AddPost.as_view(), name='post_create'),
    path('create/<int:pk>', ChangePost.as_view(), name='post_update'),
    path('delete/<int:pk>', DeletePost.as_view(), name='post_delete'),

    path('author/', upgrade_me, name='post_author'),
    path('subscribe/<int:category_id>', subscribe_me, name='subscribe'),
    path('unsubscribe/<int:category_id>', unsubscribe_me, name='unsubscribe'),

]
