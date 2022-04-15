from django.db import models
# Create your models here.

class Assistants(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=30)
    phone=models.CharField(max_length=30)
    lab_pic=models.FileField(upload_to='profile',default='lab.png')


    def __str__(self):
        return self.email


