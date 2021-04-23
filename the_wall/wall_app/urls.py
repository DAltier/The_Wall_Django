from django.urls import path
from . import views

urlpatterns = [
  path('', views.index),
  path('register', views.register),
  path('login', views.login),
  path('logout', views.logout),
  path('wall', views.wall),
  path('new_message/<int:user_id>', views.new_message),
  path('new_comment', views.new_comment),
  path('delete_message', views.delete_message),
]