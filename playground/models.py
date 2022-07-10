from pickle import TRUE
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class playground(models.Model):
    name=models.CharField(max_length=250)
    description =models.TextField(null=True,blank=True)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.name
class Fan(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self): 
        return self.name

class Games(models.Model):
    fan=models.ForeignKey(Fan,on_delete=models.SET_NULL,null=TRUE)
    User=models.ForeignKey(User,on_delete=models.CASCADE)
    playground=models.ForeignKey(playground,on_delete=models.CASCADE)
    types=models.TextField() 
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True) 

    def __str__(self) :
        return self.types[0:50]      