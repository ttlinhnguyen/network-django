
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post", views.new_post, name="post"),
    path("profile/<str:user>", views.profile, name="profile"),
    path("edit/<int:postid>", views.edit, name="edit"),

    path("like/<int:post_id>", views.like, name="like"),
    path("following", views.following, name='following')
]
