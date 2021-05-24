from django.db import models
import re
# Create your models here.
class UserManager(models.Manager):
    def validate(self, form):
        errors = {}
        if len(form['firstName']) < 2:
            error['firstName'] = "First Name must be at least 2 characters"

        if len(form['lastName']) < 2:
            error['lastName'] = "Last Name must be at least 2 characters"

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(form['email']):
            errors['email'] = 'Invalid Email Format'

        emailCheck = self.filter(email=form['email'])
        if emailCheck:
            errors['email'] = 'Email address is already in use'

        if len(form['password']) < 5:
            errors['password'] = 'Password must be at least 8 characters long'

        if form['password'] != form['confirm']:
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