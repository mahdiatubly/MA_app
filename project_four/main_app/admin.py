from django.contrib import admin
from .models import Profile, Post, Comment
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class PostInline(admin.StackedInline):
    model = Post
    # can_delete = False


class CommentInline(admin.StackedInline):
    model = Comment
    can_delete = False


class AccountUserAdmin(AuthUserAdmin):
    inlines = [ProfileInline, PostInline, CommentInline]


admin.site.unregister(User)
admin.site.register(User, AccountUserAdmin)


# Register your models here.
