from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/Customer/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
   
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.first_name
    


class Submit_claim(models.Model):
    name = models.CharField(max_length=255,null=True,blank=True)
    email =  models.CharField(max_length=255,null=True,blank=True)
    phonenumber = models.IntegerField()
    policynumber = models.CharField(max_length=255,null=True,blank=True)
    claim_type = models.CharField(max_length=255,null=True,blank=True)
    description = models.CharField(max_length=255,null=True,blank=True)
    dateofincident =  models.DateField(null=True, blank=True)
    location = models.CharField(max_length=255,null=True, blank=True)
    witnessinformation = models.CharField(max_length=255,null=True, blank=True)
    vehicleproperty = models.CharField(max_length=255,null=255,blank=255)
    policereport =  models.FileField()
    injuryinformation = models.CharField(max_length=255,null=True,blank=True)
    uploadphotos = models.FileField()
    additionalcomment = models.TextField()

    def __str__(self):
        return self.name
    
class ApplyPolicy(models.Model):
    marque =  models.CharField(max_length=255,null=True,blank=True)
    platenumnber =  models.CharField(max_length=255,null=True,blank=True)
    yearofmanufacture =  models.CharField(max_length=255,null=True,blank=True)
    insuredvalue = models.CharField(max_length=255,null=True,blank=True)
    territoriallimit = models.CharField(max_length=255,null=True,blank=True)
    deductible = models.CharField(max_length=255,null=True,blank=True)
    model = models.CharField(max_length=255,null=True,blank=True)
    numberofchasis =  models.CharField(max_length=255,null=True,blank=True)
    seatcapacity = models.CharField(max_length=255,null=True,blank=True)
    typeofvehicle = models.CharField(max_length=255,null=True,blank=True)
    occupantcover =  models.CharField(max_length=255,null=True,blank=True)
    policystatus = models.CharField(max_length=255,null=True,blank=True)
    applyid = models.ForeignKey('insurance.Policy', on_delete=models.CASCADE)

    def __str__(self):
        return self.marque

