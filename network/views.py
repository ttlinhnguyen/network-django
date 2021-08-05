import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.http import JsonResponse, Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post, Like


def index(request):
    if request.user.is_authenticated:
        post_liked = Like.objects.filter(like_person=request.user)
    else:
        post_liked = 0
    posts = Post.objects.order_by("-timestamp").all().filter(archived=False)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return render(request, "network/index.html", {
        "posts": posts,
        "post_liked": post_liked
    })

@csrf_exempt
def edit(request, postid):
    if request.method=="GET":
        return render(request, "network/edit.html", {
            "post": Post.objects.get(pk=postid)
        })
    if request.method=='POST':
        content = request.POST["edit-content"]
        if content != '':        
            post = Post.objects.get(pk=postid)
            post.content = content
            post.save()
            return redirect("index")
        else:
            return redirect("index")
    
@csrf_exempt
@login_required
def new_post(request):
    if request.method == "POST":
        content = request.POST["content"]
        if content != '':        
            Post.objects.create(user=request.user, content=content).save()
            return redirect("index")
        else:
            return redirect("index")

@csrf_exempt
def like(request, post_id):
    if request.method == 'GET':
        like_count = Like.objects.filter(post_id=post_id).count()
        return JsonResponse({
            "like_count": like_count
        }, safe=False)
    if request.method == 'PUT':
        post = Post.objects.get(pk=post_id)
        query = Like.objects.filter(like_person=request.user, post_id=post)
        if query.count() == 0:
            Like.objects.create(like_person=request.user, post_id=post).save()
        else:
            query.delete()
        return HttpResponse(status=204)

def profile(request, user):

    user = User.objects.get(username=user)

    following = user.following.all()
    if_contain = User.objects.filter(pk=request.user.id, following__id=user.id).count()
    if if_contain != 0:
        if_follow = True
    else:
        if_follow = False


    if request.method=='POST':
        follow_this_user = User.objects.get(pk=user.id)
        if if_follow:       
            request.user.following.remove(follow_this_user)
        else:
            request.user.following.add(follow_this_user)
        return redirect(reverse('profile', args=[user]))

    posts = Post.objects.order_by("-timestamp").all().filter(user=user.id)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    followers = User.objects.filter(following=user.id).count()
    return render(request, "network/profile.html", {
        "username": user.username,
        "posts": posts,
        "following": len(following),
        "if_follow": if_follow,
        "followers": followers
    })

def following(request):
    following_users = request.user.following.all()
    posts = Post.objects.filter(user__in=following_users)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return render(request, "network/following.html", {
        "posts": posts
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
