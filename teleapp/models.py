from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=False,unique=False)
    name = models.CharField(max_length=150, null=False, blank=False)
    password = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(unique=True, blank=True,null=True)

    class Meta:
        db_table = 'CustomUser'
    def __str__(self):
        return self.name if self.name else self.email
    
class GlobalNumbers(models.Model):
    name = models.CharField(max_length=1000,blank=False,null=False)
    phone_number = models.BigIntegerField(blank=False,null=False)
    user = models.ForeignKey(CustomUser,blank=True,null=True,on_delete=models.SET_NULL)
    is_spam = models.BooleanField(default = False)