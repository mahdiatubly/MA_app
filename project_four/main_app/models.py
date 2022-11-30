from django.db import models
from django.db import models
# Import the reverse function
from django.urls import reverse
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)
    interest = models.TextField(max_length=250)
    comments = models.TextField

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class Post(models.Model):
    topic = models.TextField(max_length=200, blank=True,
                             null=True, editable=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    post_content = models.TextField
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, blank=True, null=True, default='', editable=True)
    upvotes = models.IntegerField
    downvotes = models.IntegerField(blank=True, null=True, editable=True)
    updates = models.TextField(blank=True, null=True, editable=True)


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
    feedback = models.TextField
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, blank=True, null=True, default='',  editable=True)
    upvotes = models.IntegerField
    downvotes = models.IntegerField
    Post = models.ForeignKey(
        Post, on_delete=models.CASCADE, blank=True, null=True, default='',  editable=True)


class downvoted_commentts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Comment, on_delete=models.CASCADE)


class upvoted_commentts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Comment, on_delete=models.CASCADE)
# Create your models here.
