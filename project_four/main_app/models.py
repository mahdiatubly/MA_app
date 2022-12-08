from django.db import models
from django.db import models
# Import the reverse function
from django.urls import reverse
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser


levels = (('Select', 's'), ('Beginner', 'b'),
          ('Intermediate', 'i'), ('Advance', 'a'))


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)
    interest = models.TextField(max_length=250)
    rate = models.FloatField

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class Post(models.Model):
    field = models.CharField(
        max_length=200, editable=True, default='General', blank=True, null=True)
    topic = models.CharField(
        max_length=200, editable=True, default='General', blank=True, null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=True, blank=True, null=True)
    level = models.CharField(
        max_length=200, editable=True, default='Beginner', blank=True, null=True)
    lesson = models.TextField(blank=True, null=True, editable=True)
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, blank=True, null=True, default='', editable=True)
    upvotes = models.IntegerField(blank=True, null=True, editable=True)
    downvotes = models.IntegerField(blank=True, null=True, editable=True)
    updates = models.TextField(blank=True, null=True, editable=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('', kwargs={'pk': self.id})


class saved_content(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Post, on_delete=models.CASCADE)


class upvoted_posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Post, on_delete=models.CASCADE)


class downvoted_posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default='')
    feedback = models.TextField(blank=True, null=True, editable=True)
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, blank=True, null=True, default='',  editable=True)
    upvotes = models.IntegerField(blank=True, null=True, editable=True)
    downvotes = models.IntegerField(blank=True, null=True, editable=True)
    Post = models.ForeignKey(
        Post, on_delete=models.CASCADE, blank=True, null=True, default='',  editable=True)


class downvoted_commentts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Comment, on_delete=models.CASCADE)


class upvoted_commentts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Comment, on_delete=models.CASCADE)

### -----------------------------------###-------------------------------------###


# class User(AbstractUser):
#     name = models.CharField(max_length=200, null=True)
#     email = models.EmailField(unique=True, null=True)
#     bio = models.TextField(null=True)

#     avatar = models.ImageField(null=True, default="avatar.svg")

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    # This meta class is to show the most recent messages in the top.
    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    # This meta class is to show the most recent messages in the top.
    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]
