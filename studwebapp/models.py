from operator import mod
from django.db import models
from django.contrib.auth.models import User
from distutils.command.upload import upload

# Create your models here.
class Tutor(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    user_address=models.CharField(max_length=255)
    user_gender=models.CharField(max_length=150)
    user_mobile=models.CharField(max_length=255)
    user_photo=models.ImageField(upload_to='image/',null=True)
    def __str__(self):
    
        return self.user.username

class course(models.Model):
    #course = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    course_name = models.CharField(max_length=225)
    fee = models.IntegerField()

    def __str__(self):
        return self.course_name

class student(models.Model):
    course = models.ForeignKey(course, on_delete=models.CASCADE, null=True)
    std_name =models.CharField(max_length=225)
    std_address =models.CharField(max_length=225)
    std_age =models.IntegerField()
    Join_date =models.DateField()

    def __str__(self):
        return self.std_name
    

