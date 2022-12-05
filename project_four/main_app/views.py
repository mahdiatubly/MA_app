from django.shortcuts import render, redirect
# Add the following import
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Post, Profile, Comment, Room, Topic, Message
from django.db.models import Q
from .forms import PostForm
# from .models import User


# Add the following import
from django.http import HttpResponse

# views.py
from django.views.generic import ListView

# Define the home view


def home(request):
    return render(request, 'home.html')


def se(request):
    return render(request, 'se.html')


class PostCreate(CreateView):
    model = Post
    fields = ['field', 'topic', 'level', 'lesson']
    success_url = '/'

    def form_valid(self, form):
        # Assign the logged in user
        form.instance.upvotes = 0
        form.instance.downvotes = 0
        form.instance.updates = ''
        form.instance.user = self.request.user
        form.instance.profile = Profile.objects.get(user=self.request.user)
        return super(PostCreate, self).form_valid(form)


class PostUpdate(UpdateView):
    model = Post
    fields = ['field', 'topic', 'level', 'lesson']
    success_url = '/'


class PostDelete(DeleteView):
    model = Post
    fields = ['field', 'topic', 'level', 'lesson']
    success_url = 'home'


def signup(request):
    context = {"error": False}
    if request.method == "GET":
        return render(request, 'main_app/signup.html', context)
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        try:
            user = User.objects.create_user(
                first_name=first_name, last_name=last_name, username=username,
                password=password, email=email)
            if user is not None:
                # run the login method to automatically log in user
                # as they sign up.
                return signin(request)
        except:
            context["error"] = f"Username '{username}' already exists."
            return render(request, 'main_app/signup.html', context)


def signin(request):
    context = {"error": False}
    if request.method == "GET":
        return render(request, 'main_app/signin.html')
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')


def signout(request):
    auth.logout(request)
    return redirect('/')


def get_se_content_bg(request):
    try:
        se_content = Post.objects.filter(
            field='Software Engineering', level='Beginner')
    except:
        se_content = 'New Content will be added soon'
    return render(request, 'se_levels.html', {'content': se_content})


def get_se_content_md(request):
    try:
        se_content = Post.objects.filter(
            field='Software Engineering', level='Intermediate')
    except:
        se_content = 'New Content will be added soon'
    return render(request, 'se_levels.html', {'content': se_content})


def get_se_content_ad(request):
    try:
        se_content = Post.objects.filter(
            field='Software Engineering', level='Advance')
    except:
        se_content = 'New Content will be added soon'
    return render(request, 'se_levels.html', {'content': se_content})


def lesson(request, pk):
    try:
        lesson = Post.objects.get(
            id=pk)
    except:
        lesson = 'We are working on making this lesson available as soon as possible'
    return render(request, 'lesson.html', {'lesson': lesson})


### -------------------------------###-----------------------------------###

def chatting_home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q))[0:3]

    context = {'rooms': rooms, 'topics': topics,
               'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'main_app/chatting_home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}
    return render(request, 'base/room.html', context)
