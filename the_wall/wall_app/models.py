from django.db import models
import re
import bcrypt


# User Registration Manager
class UserManager(models.Manager):
  def registration_validator(self, post_data):
    errors = {}
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    LETTER_REGEX = re.compile(r'^[a-zA-Z]*$')


    # Validate name data
    if not LETTER_REGEX.match(post_data['first_name']) or len(post_data['first_name']) < 2 :
      errors['first_name'] = "The first name field is required and should be at least 2 letters long."
    if not LETTER_REGEX.match(post_data['last_name']) or len(post_data['last_name']) < 2:
      errors['last_name'] = "The last name field is required and should be at least 2 letters long."


    # Validate email data
    if not EMAIL_REGEX.match(post_data['email']):
      errors['email'] = ("Invalid or missing email address!")
    if User.objects.filter(email = post_data['email']).exists():
      errors['email'] = ("Email already exists, try logging in.")


    # Validate password data
    if len(post_data['password']) < 8:
      errors['password'] = "The password field is required and should be at least 8 characters long."
    if post_data['password'] != post_data['confirm_password']:
      errors['confirm_password'] = "Your passwords do not match, try again!"

    return errors


  def login_validator(self, post_data):
    errors = {}

    user_list = User.objects.filter(email = post_data['email'])
    if len(user_list) > 0:
      user = user_list[0]
      if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
        errors['password'] = "Invalid Credentials"
    else:
      errors['email'] = "Invalid Credentials"
      
    return errors

# User model
class User(models.Model):
  first_name = models.CharField(max_length=255)
  last_name = models.CharField(max_length=255)
  email = models.CharField(max_length=255)
  password = models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = UserManager()

  def __repr__(self):
    return f"<User Object: {self.id} {self.first_name} {self.last_name}"


# Message Manager
class MessageManager(models.Manager):
  def validator(self, post_data):
    errors = {}
    if len(post_data['message']) < 10:
      errors['message'] = "Your message should be at least 10 characters long"
    return errors


# Message model
class Message(models.Model):
  message = models.TextField()
  user = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = MessageManager()

  def __repr__(self):
    return f"<Message Object: {self.id} {self.message}>"


# Comment Manager
class CommentManager(models.Manager):
  def validator(self, post_data):
    errors = {}
    if len(post_data['comment']) == 00:
      errors['comment'] = "Your comment should be at least be 1 characters long"
    return errors


# Comment model
class Comment(models.Model):
  comment = models.TextField()
  user = models.ForeignKey(User, related_name="user_comments", on_delete=models.CASCADE)
  message = models.ForeignKey(Message, related_name="message_comments", on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = CommentManager()

  def __repr__(self):
    return f"<Comment Object: {self.id} {self.comment}>"