from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
import datetime


class WishManager(models.Manager):


    def basic_validator(self, postData):
        errors = {}
        if len(postData['item']) < 3 and len(postData['item']) > 0:
            errors["item"] = "item cannot be less than 3 characters"
        if len(postData['item']) == 0:
            errors["item"] = "item cannot be blank"
        if len(postData['desc']) == 0:
            errors["desc"] = "description cannot be blank"
        if len(postData['desc']) < 3 and len(postData['desc']) > 0:
            errors["desc"] = "description cannot be less than 3 characters"
        if len(postData['item']) > 100:
            errors["item"] = "item cannot be over 100 characters"
        if len(postData['desc']) > 100:
            errors["desc"] = "description cannot be over 100 characters"
        return errors

    def Create_wish(self,postData,user):
        this_user=User.objects.get(email=user.email)
        Wish.objects.create(item=postData['item'],desc=postData['desc'],author=this_user)

    def Update_wish(self,postData,wishid):
        this_wish=Wish.objects.get(id=wishid)
        this_wish.item=postData['item']
        this_wish.desc=postData['desc']
        this_wish.save()

    def Delete_wish(self,wishid):
        this_wish=Wish.objects.get(id=wishid)
        this_wish.delete()
#------------------------------------------------------------------------
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        user=User.objects.all().values().filter(email=postData['email'])
        if user:
            errors["user"] = "email already exists in database"
        if len(postData['firstname']) < 2:
            errors["firstname"] = "firstname cannot be less than 2 characters"
        if postData['firstname'].isalpha() is False:
            errors["firstname"] = "first name cannot contain numbers"
        if len(postData['firstname']) > 100:
            errors["firstname"] = "first name cant be over 100 characters"
        if len(postData['lastname']) < 2:
            errors["lastname"] = "last name must be longer than 2 characters"
        if len(postData['lastname']) > 100:
            errors["lastname"] = "last name cant be over 100 characters" #ADD MAX LENGTH VALIDATIONS OM ALL
        if postData['lastname'].isalpha() is False:
            errors["lastname"] = "last name cannot contain numbers"
        if len(postData['password']) < 8 :
            errors["password"] = "password cannot be less than 8 characters"
        if len(postData['password']) > 100 :
            errors["password"] = "password cannot be over 100 characters"
        if postData['password'] != postData['passwordconf'] :
            errors["passwordconf"] = "passwords do not match"
        if len(postData['email']) > 150 :
            errors["email"] = "email cannot be over 150 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "email is invalid"
        return errors

    def login_validator(self, postData):
        errors = {}
        if len(postData['password']) < 1 :
            errors["password"] = "please enter your password"
        try:
            user=User.objects.all().values().get(email=postData['email'])
            if user:
                if bcrypt.checkpw(postData['password'].encode(), user['pwhash'].encode()):
                    print("password match")
                else:
                    errors["password"] = "passwords do not match"
                return errors
        except:
            errors['login']="user does not exist in database"
            return errors
    def Create_user(self,postData):
        user = User.objects.create()
        user.firstname = postData['firstname']
        user.lastname = postData['lastname']
        user.email = postData['email']
        user.pwhash = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        user.save()
#------------------------------------------------------------------------
class User(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    pwhash = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # *************************
    # Connect an instance of UserManager to our User model overwriting
    # the old hidden objects key with a new one with extra properties!!!
    objects = UserManager()
    # *************************
#------------------------------------------------------------------------
class Wish(models.Model):
    item = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    granted= models.BooleanField(default=False)
    likes=models.ManyToManyField(User, related_name='liked')
    author=models.ForeignKey(User,related_name='uploaded')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=WishManager()

