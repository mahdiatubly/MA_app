from django.urls import path, include
from . import views
from .views import PostCreate
from django.conf.urls import url
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('chatting/', views.chatting, name="chat"),
    path('create-room/', views.createRoom, name='create-room'),
    path('room/<str:pk>/', views.room, name="room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    # path('update-user/<str:pk>/', views.userProfile, name="update-user"),
    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),

    path('software/engineering/', views.se, name='se'),
    path('software/engineering/level1', views.get_se_content_bg, name='se_1'),
    path('software/engineering/level1/<str:pk>', views.lesson, name='lesson'),
    path('software/engineering/level1/<str:pk>/update/',
         views.updateLesson, name='lesson_update'),
    path('software/engineering/level1/<str:pk>/delete/',
         views.deleteLesson, name='lesson_delete'),
    path('software/engineering/level2', views.get_se_content_md, name='se_2'),
    path('software/engineering/level3', views.get_se_content_ad, name='se_3'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('add/', views.PostCreate.as_view(), name='add'),
]
