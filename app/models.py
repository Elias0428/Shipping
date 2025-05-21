
from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser

class Numbers(models.Model):
    phone_number = models.BigIntegerField()  
    created_at = models.DateTimeField(auto_now_add=True) 
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'numbers'

class Users(AbstractUser):

    ROLES_CHOICES = (
        ('A', 'Agent'),
        ('S', 'Supervisor'),
        ('C', 'Customer'),
        ('SUPP', 'Supplementary'),
        ('AU', 'Auditor'),
        ('TV', 'Tv'),
        ('Admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLES_CHOICES)
    assigned_phone = models.ForeignKey(Numbers, on_delete=models.SET_NULL, null=True, blank=True)
    # Sobrescribimos solo el campo email
    email = models.EmailField(
        blank=True, 
        null=True,
        unique=False
    )
    
    class Meta:
        db_table = 'users'
        
    def _str_(self):
        return self.username

class Clients(models.Model):
    agent = models.ForeignKey(Users, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.BigIntegerField()
    email = models.EmailField()
    address = models.CharField(max_length=255)
    zipcode = models.IntegerField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    county = models.CharField(max_length=100, null=True)
    date_birth = models.DateField()  
    is_active = models.BooleanField(default=True)  
    created_at = models.DateTimeField(auto_now_add=True) 

    class Meta:
        db_table = 'clients'

    def _str_(self):
        return f'{self.first_name} {self.last_name} - {self.phone_number}'

class Shipping(models.Model):
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    status_date = models.DateField()
    description = models.TextField(null=True)
    country = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'shipping'

class Packages(models.Model):
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    shipping = models.ForeignKey(Shipping, on_delete=models.CASCADE)
    agent = models.ForeignKey(Users, on_delete=models.CASCADE)
    type = models.CharField(max_length=200)
    load = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'packages'


class DropDownList(models.Model):
    statusShipping = models.TextField(null=True)   
    country =  models.TextField(null=True)   

    class Meta:
        db_table = 'drop_down_list'


from .modelsSMS import *
