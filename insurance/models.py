from django.db import models
from django.contrib.auth.models import User
from customer.models import Customer

class Category(models.Model):
    category_name =models.CharField(max_length=30)
    creation_date =models.DateField(auto_now=True)
    def __str__(self):
        return self.category_name

class Policy(models.Model):
     VEHICLE_CHOICES = [
        ('person_goods_transport', 'Person & Goods Transport Cars'),
        ('minibus', 'Minibus & Minibus Carrying Goods'),
        ('motorcycle', 'Motorcycles'),
        ('bus', 'Buses'),
        ('truck', 'Trucks'),
        ('van', 'Van Vehicles'),
        ('driving_school', 'Driving School Vehicles'),
        ('trailer_semi_trailers', 'Trailer & Semi-Trailers'),
        ('tractor', 'Tractor'),
        ('Crop', 'Crop Insurance'),
        ('Forestry', 'Forestry Insurance'),
        ('Warehouse', 'Warehouse Receipt Insurance'),
        ('Equipment', 'Equipment Insurance'),
      
    ]
     
     category = models.ForeignKey(Category, on_delete=models.CASCADE)
     policy_name = models.CharField(max_length=200)
     type_of_vehicle = models.CharField(max_length=255,choices=VEHICLE_CHOICES)
     premium_amount = models.PositiveIntegerField()
     deductible = models.PositiveIntegerField()
     tenure = models.PositiveIntegerField()
     creation_date = models.DateField(auto_now=True)
     def __str__(self):
        return self.policy_name

class PolicyRecord(models.Model):
    customer= models.ForeignKey(Customer, on_delete=models.CASCADE)
    Policy= models.ForeignKey(Policy, on_delete=models.CASCADE)
    status = models.CharField(max_length=100,default='Pending')
    creation_date =models.DateField(auto_now=True)
    def __str__(self):
        return self.Policy.policy_name

class Question(models.Model):
    customer= models.ForeignKey(Customer, on_delete=models.CASCADE)
    description =models.CharField(max_length=500)
    admin_comment=models.CharField(max_length=200,default='Nothing')
    asked_date =models.DateField(auto_now=True)
    def __str__(self):
        return self.description