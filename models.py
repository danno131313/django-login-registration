from django.db import models
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.

class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if (len(postData['first_name']) < 1 or len(postData['last_name']) < 1):
            errors['name'] = "First and last names must not be empty"
        if not EMAIL_REGEX.match(postData['email_address']):
            errors['email'] = "Must be a valid email address"
        if User.objects.filter(email_address=postData['email_address']):
            errors['usedEmail'] = "Email address already in use"
        if len(postData['password']) < 8:
            errors['pwlength'] = "Password must be at least 8 characters"
        elif postData['password'] != postData['password_confirm']:
            errors['pw'] = "Password didn't match"
        return errors

class User(models.Model):
    first_name    = models.CharField(max_length=255)
    last_name     = models.CharField(max_length=255)
    email_address = models.CharField(max_length=255)
    password      = models.CharField(max_length=255)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    objects = UserManager()
