from django.urls import path, include
from . import views
from .views import PostCreate
from django.conf.urls import url
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('chatting/', views.chatting_home, name="chat"),
    path('software/engineering/', views.se, name='se'),
    path('software/engineering/level1', views.get_se_content_bg, name='se_1'),
    path('software/engineering/level1/<str:pk>', views.lesson, name='lesson'),
    path('software/engineering/level1/<str:pk>/update/',
         views.PostUpdate.as_view(), name='lesson_update'),
    path('software/engineering/level1/<str:pk>/delete/',
         views.PostDelete.as_view(), name='lesson_delete'),
    path('software/engineering/level2', views.get_se_content_md, name='se_2'),
    path('software/engineering/level3', views.get_se_content_ad, name='se_3'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('add/', views.PostCreate.as_view(), name='add'),
]
