from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt
from datetime import datetime, timedelta


# Login and registration page
def index(request):
  if "user_id" in request.session:
    return redirect("/wall")
  return render(request, "index.html")


# Registration 
def register(request):
  errors = User.objects.registration_validator(request.POST)
  if len(errors) > 0:
    for key, value in errors.items():
        messages.error(request, value)
    return redirect("/")
  else:
    hash_slinging_slasher = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    new_user = User.objects.create(
      first_name = request.POST['first_name'], 
      last_name = request.POST['last_name'], 
      email = request.POST['email'], 
      password = hash_slinging_slasher
    )

    request.session['user_id'] = new_user.id

    return redirect('/wall')


# Login user
def login(request):
  errors = User.objects.login_validator(request.POST)

  if len(errors) > 0:
    for key, value in errors.items():
        messages.error(request, value)
    return redirect("/")
  else:
    user = User.objects.get(email = request.POST['email'])
    request.session['user_id'] = user.id
    return redirect('/wall')


# Display wall
def wall(request):
  within_30_minutes = datetime.now() - timedelta(seconds=60 * 30)
  messages_before_30_minutes = Message.objects.filter(created_at = within_30_minutes)
  print(messages_before_30_minutes)
  if 'user_id' not in request.session:
    return redirect('/')
  context = {
    'user': User.objects.get(id=request.session['user_id']),
    'all_messages': Message.objects.all(),
    'messages_before_30_minutes': messages_before_30_minutes,
  }
  return render(request, 'wall.html', context)


# Post message to wall
def new_message(request, user_id):
  errors = Message.objects.validator(request.POST)
  if len(errors) > 0:
    for key, value in errors.items():
      messages.error(request, value)
    return redirect('/wall')
  else:
    user = User.objects.get(id=user_id)
    Message.objects.create(message=request.POST['message'], user=user)
    return redirect('/wall')


# Post comment to wall
def new_comment(request):
  errors = Comment.objects.validator(request.POST)
  if len(errors) > 0:
    for key, value in errors.items():
      messages.error(request, value)
    return redirect('/wall')
  else:
    user = User.objects.get(id=request.POST['user_id'])
    message = Message.objects.get(id=request.POST['message_id'])
    Comment.objects.create(comment=request.POST['comment'], message=message, user=user)
    return redirect('/wall')


# Delete message
def delete_message(request):
  message_to_be_deleted = Message.objects.get(id=request.POST['delete_message_id'])
  message_to_be_deleted.delete()
  return redirect('/wall')


# Logout user
def logout(request):
  del request.session['user_id']
  return redirect('/')