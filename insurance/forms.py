from django import forms
from django.contrib.auth.models import User
from . import models

class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 8}))


class CategoryForm(forms.ModelForm):
    class Meta:
        model=models.Category
        fields=['category_name']

from django import forms
from .models import Policy

class PolicyForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=models.Category.objects.all(), empty_label="Category Name", to_field_name="id", widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Medial Insurance'}))
    policy_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Comprehensive insurance'}))
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

    type_of_vehicle = forms.ChoiceField(choices=VEHICLE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    premium_amount = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '5000'}))
    deductible = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '5000'}))
    tenure = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '12'}))

    class Meta:
        model = Policy
        fields = ['category', 'policy_name', 'type_of_vehicle','premium_amount', 'deductible', 'tenure']


class QuestionForm(forms.ModelForm):
    class Meta:
        model=models.Question
        fields=['description']
        widgets = {
        'description': forms.Textarea(attrs={'rows': 6, 'cols': 30})
        }