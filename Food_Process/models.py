from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class FoodProcess(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    video = models.FileField(upload_to='videos/')

    def __str__(self):
        return self.name


# LoginRecord 
class LoginRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True) 

# staff CRUD Operations for Foods 
class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="food_images/", blank=True, null=True)
    video = models.FileField(upload_to="food_videos/", blank=True, null=True)

    def __str__(self):
        return self.name 

# for Contacts 
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"