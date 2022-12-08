from django.shortcuts import render, redirect
from django.contrib import messages
# Add the following import
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Post, Profile, Comment, Room, Topic, Message, User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .forms import PostForm, RoomForm
# from .models import User


# Add the following import
from django.http import HttpResponse

# views.py
from django.views.generic import ListView

# Define the home view


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    posts = Post.objects.filter(
        Q(topic__icontains=q) |
        Q(field__icontains=q) |
        Q(lesson__icontains=q)
    )
    posts_count = posts.count()
    lessons = Post.objects.all()
    context = {'lessons': posts, 'q_value': q, 'posts_count': posts_count}
    return render(request, 'home.html', context)


def se(request):
    return render(request, 'se.html')


class PostCreate(LoginRequiredMixin, CreateView):
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


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['field', 'topic', 'level', 'lesson']
    success_url = '/'

    def form_valid(self, form):
        # Assign the logged in user
        form.instance.user = self.request.user
        return super(PostCreate, self).form_valid(form)


@login_required(login_url='signin')
def updateLesson(request, pk):
    lesson = Post.objects.get(id=pk)
    form = PostForm(instance=lesson)
    if request.user != lesson.user:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        lesson.field = request.POST.get('field')
        lesson.topic = request.POST.get('topic')
        # topic = lesson.objects.get_or_create(topic=lesson_topic)
        # lesson.topic = topic
        lesson.lesson = request.POST.get('lesson')
        lesson.save()
        return redirect('home')

    context = {'form': form}
    return render(request, 'main_app/update_form.html', context)


# class PostDelete(LoginRequiredMixin, DeleteView):
#     model = Post
#     fields = ['field', 'topic', 'level', 'lesson']
#     success_url = '/'

@login_required(login_url='login')
def deleteLesson(request, pk):
    lesson = Post.objects.get(id=pk)

    if request.user != lesson.user:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        lesson.delete()
        return redirect('home')
    return render(request, 'main_app/delete.html', {'obj': lesson})


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
            user.username = user.username.lower()
            user.save()
            if user is not None:
                # run the login method to automatically log in user
                # as they sign up.
                return signin(request)
        except:
            context["error"] = f"Username '{username}' already exists."
            return render(request, 'main_app/signup.html', context)


def signin(request):

    if request.user.is_authenticated:
        return redirect('home')

    context = {"error": False}
    if request.method == "GET":
        return render(request, 'main_app/signin.html')

    if request.method == "POST":
        username = request.POST["username"].lower()
        password = request.POST["password"]
    try:
        user = User.objects.get(username=username)
    except:
        messages.error(request, 'User does not exist')

    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)
        return redirect('/')
    else:
        messages.error(request, 'Username OR password does not exit')


def signout(request):
    auth.logout(request)
    return redirect('home')


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
    return render(request, 'lesson.html', {'lesson': lesson, 'reqs': request})


### -------------------------------###-----------------------------------###

def chatting(request):
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
    return render(request, 'main_app/room.html', context)


@login_required(login_url='signin')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'main_app/room_form.html', context)


# class CreateRoom(CreateView):
#     model = Room
#     fields = '__all__'
#     success_url = '/'

#     def form_valid(self, form):
#         # Assign the logged in user
#         form.instance.topic = Topic.objects.all()


@login_required(login_url='signin')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'main_app/room_form.html', context)


# class UpdateRoom(UpdateView):
#     model = Room
#     fields = '__all__'
#     success_url = '/'

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'main_app/delete.html', {'obj': room})


# class DeleteRoom(DeleteView):
#     model = Room
#     fields = '__all__'
#     success_url = '/'


@login_required(login_url='signin')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})


@login_required(login_url='signin')
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms,
               'room_messages': room_messages, 'topics': topics}
    return render(request, 'main_app/profile.html', context)


# @login_required(login_url='login')
# def updateUser(request):
#     pass
#     user = request.user
#     form = UserForm(instance=user)

#     if request.method == 'POST':
#         form = UserForm(request.POST, request.FILES, instance=user)
#         if form.is_valid():
#             form.save()
#             return redirect('user-profile', pk=user.id)

#     return render(request, 'base/update-user.html', {'form': form})


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'main_app/topics.html', {'topics': topics})


def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'main_app/activity.html', {'room_messages': room_messages})
