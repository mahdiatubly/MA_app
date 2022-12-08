from django.forms import ModelForm
from .models import Post, Room, Profile
from django.contrib.auth.forms import UserCreationForm


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['upvotes', 'downvotes', 'user', 'profile', 'updates']

# class MyUserCreationForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['name', 'username', 'email', 'password1', 'password2']


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']


# class UserForm(ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['avatar', 'name', 'username', 'email', 'bio']


# class UserForm(ModelForm):
#     class Meta:
#         model = User
#         fields = ['avatar', 'name', 'username', 'email', 'bio']
