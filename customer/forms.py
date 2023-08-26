from django import forms
from django.contrib.auth.models import User
from . import models
# from .models import ApplyPolicyAgriculture, ApplyPolicyProperty, ApplyPolicyMedical


class CustomerUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class CustomerForm(forms.ModelForm):
    class Meta:
        model=models.Customer
        fields=['address','mobile','profile_pic','email','nationalid']


# class PolicyAgricultureForm(forms.ModelForm):
#     class Meta:
#         model = ApplyPolicyAgriculture
#         fields = '__all__'

# class PolicyPropertyForm(forms.ModelForm):
#     class Meta:
#         model = ApplyPolicyProperty
#         fields = '__all__'

# class PolicyMedicalForm(forms.ModelForm):
#     class Meta:
#         model = ApplyPolicyMedical
#         fields = '__all__'
