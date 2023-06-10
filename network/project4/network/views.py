from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Post


from .models import User


def index(request):
    return render(request, "network/index.html")


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


# create post
def new_post(request):
    if request.method == "POST":
        text = request.POST["text"]
        user = request.user
        # create new post object
        post = Post.objects.create(pub_user = user , Post_text = text)
        post.save()
    else:
        return render(request, "network/new.html")
    
    return render(request, "network/index.html")

# view all posts
def view_all(request):
    #retrieve all posts ordered from latest 
    posts = Post.objects.all().order_by('-pub_dateTime')
    return render(request, "network/allPosts.html", {"posts":posts})


#user profile page
def profile_view(request, username):
    # retrieve the profile user and posts
    user = User.objects.get(username=username)
    # retrieve user's posts
    posts = Post.objects.filter(pub_user = user).order_by('-pub_dateTime')
    # retrieve user's followers and following count
    followers_num = user.followers.all().count()
    following_num = user.following.all().count()
    #checks if the requesting user is following the profile user
    is_following = request.user.following.filter(username=username).exists()

    return render(request, "network/profile.html" , {"username" : user.username , "posts": posts, "followers": followers_num, "following": following_num, "is_following":is_following})

# follow
def follow(request,username):
    user= request.user
    following_user = User.objects.get(username=username)
    user.following.add(following_user)
    return render(request, "network/index.html")

#unfollow
def unfollow(request, username):
    user =request.user
    following_user = User.objects.get(username=username)
    user.following.remove(following_user)
    return render(request, "network/index.html")