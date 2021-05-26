from django.db import models
import re
import bcrypt
# Create your models here.
class UserManager(models.Manager):
    def validate(self, postData):
        errors = {}
        #length of first name
        if len(postData['firstName']) < 2:
            errors['firstName'] = "First Name must be at least 2 characters"
        #length of last name
        if len(postData['lastName']) < 2:
            errors['lastName'] = "Last Name must be at least 2 characters"
        # email match format
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Invalid Email Format'
        # email is unique check
        emailCheck = self.filter(email=postData['email'])
        if emailCheck:
            errors['email'] = 'Email address is already in use'
        # password  length
        if len(postData['password']) < 5:
            errors['password'] = 'Password must be at least 5 characters long'

        if postData['password'] != postData['confirm']:
            errors['password'] = 'Password do not match'
        return errors

class User(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Movie(models.Model):
    title = models.CharField(max_length=255)
    network = models.CharField(max_length=45)
    description = models.TextField(max_length=255)
    release_date = models.DateTimeField()
    users = models.ManyToManyField(User, related_name = 'movies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)