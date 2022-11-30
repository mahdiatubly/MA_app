from django.urls import path, include
from . import views
from .views import PostCreate
from django.conf.urls import url
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('software/engineering/', views.se, name='se'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('add/', views.PostCreate.as_view(), name='add'),
]
