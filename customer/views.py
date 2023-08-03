from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.db.models import Q
from django.core.mail import send_mail
from insurance import models as CMODEL
from insurance import forms as CFORM
from django.contrib.auth.models import User
from customer.models import *
from django.contrib import messages
from insurance.models import Policy
from .forms import PolicyAgricultureForm, PolicyPropertyForm, PolicyMedicalForm

def index_home(request):
    return render(request,'index.html')


def customerclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'customer/customerclick.html')


def customer_signup_view(request):
    userForm=forms.CustomerUserForm()
    customerForm=forms.CustomerForm()
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST)
        customerForm=forms.CustomerForm(request.POST,request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customer=customerForm.save(commit=False)
            customer.user=user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
        return HttpResponseRedirect('customerlogin')
    return render(request,'customer/customersignup.html',context=mydict)

def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()

@login_required(login_url='customerlogin')
def customer_dashboard_view(request):
    dict={
        'customer':models.Customer.objects.get(user_id=request.user.id),
        'available_policy':CMODEL.Policy.objects.all().count(),
        'applied_policy':CMODEL.PolicyRecord.objects.all().filter(customer=models.Customer.objects.get(user_id=request.user.id)).count(),
        'total_category':CMODEL.Category.objects.all().count(),
        'total_question':CMODEL.Question.objects.all().filter(customer=models.Customer.objects.get(user_id=request.user.id)).count(),

    }
    return render(request,'customer/customer_dashboard.html',context=dict)

def apply_policy_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    policies = CMODEL.Policy.objects.all()
    return render(request,'customer/apply_policy.html',{'policies':policies,'customer':customer})

def apply_view(request,pk):
    customer = models.Customer.objects.get(user_id=request.user.id)
    policy = CMODEL.Policy.objects.get(id=pk)
    policyrecord = CMODEL.PolicyRecord()
    policyrecord.Policy = policy
    policyrecord.customer = customer
    policyrecord.save()
    return redirect('history')

def history_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    policies = CMODEL.PolicyRecord.objects.all().filter(customer=customer)
    return render(request,'customer/history.html',{'policies':policies,'customer':customer})

def ask_question_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    questionForm=CFORM.QuestionForm() 
    
    if request.method=='POST':
        questionForm=CFORM.QuestionForm(request.POST)
        if questionForm.is_valid():
            
            question = questionForm.save(commit=False)
            question.customer=customer
            question.save()
            return redirect('question-history')
    return render(request,'customer/ask_question.html',{'questionForm':questionForm,'customer':customer})

def question_history_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    questions = CMODEL.Question.objects.all().filter(customer=customer)
    return render(request,'customer/question_history.html',{'questions':questions,'customer':customer})

def submit_claim_view(request):

    if request.method == 'POST':
        submit_claim = Submit_claim()
        submit_claim.name =  request.POST['name']
        submit_claim.email = request.POST['email']
        submit_claim.phonenumber = request.POST['phonenumber']
        submit_claim.policynumber = request.POST['claimtype'] 
        submit_claim.description = request.POST['description']
        submit_claim.dateofincident = request.POST['dateofincident']
        submit_claim.location = request.POST['location']
        submit_claim.witnessinformation = request.POST['witnessinformation']
        submit_claim.vehicleproperty =  request.POST['vehicleproperty']
        submit_claim.policereport =  request.FILES['policereport'] 
        submit_claim.injuryinformation = request.POST['injuryinformation']
        submit_claim.uploadphotos = request.FILES['uploadphotos']
        submit_claim.additionalcomment = request.POST['additionalcomment']
        submit_claim.save()
        messages.success( request,"Claims added successfully")
    return render(request,'customer/submit_claim.html')

def claim_history_view(request):
    return render(request,'customer/claim_history.html')

def moredetail_vehicle(request):
    userForm=forms.CustomerUserForm()
    customerForm=forms.CustomerForm()
    mydict={'userForm':userForm,'customerForm':customerForm}
    years = list(range(1950, 2023))
    context = {
        'years': years,
       
    }
    if request.method == 'POST':
        applyData =  ApplyPolicyVehicle()
        applyData.marque =  request.POST['marque']
        applyData.platenumnber = request.POST['platenumber']
        applyData.yearofmanufacture =  request.POST['yearofmanufacture']
        applyData.insuredvalue =  request.POST['insuredvalue']
        applyData.territoriallimit = request.POST['territoriallimit']
        applyData.deductible = request.POST['deductible']
        applyData.model = request.POST['model']
        applyData.numberofchasis = request.POST['numberofchasis']
        applyData.seatcapacity = request.POST['seatcapacity']
        applyData.typeofvehicle = request.POST['typeofvehicle']
        applyData.occupantcover = request.POST['occupantcovered']
        applyData.policystatus = request.POST['policystatus']
        # applyData.applyid = Policy.objects.get(id=id)
    return render(request,'customer/moredetail-vehicle.html',context)

def moredetail_medical(request):
    userForm=forms.CustomerUserForm()
    customerForm=forms.CustomerForm()
    mydict={'userForm':userForm,'customerForm':customerForm}
    return render(request,'customer/moredetails-medial.html',context=mydict)


def moredetail_fire(request):
    userForm=forms.CustomerUserForm()
    customerForm=forms.CustomerForm()
    mydict={'userForm':userForm,'customerForm':customerForm}
    return render(request,'customer/moredetails_fire.html',context=mydict)


def moredetail_agriculture(request):
    userForm=forms.CustomerUserForm()
    customerForm=forms.CustomerForm()
    mydict={'userForm':userForm,'customerForm':customerForm}
    return render(request,'customer/moredetails_agriculture.html',context=mydict)


def apply_policy_agriculture(request):
    if request.method == 'POST':
        form = PolicyAgricultureForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_url')  
    else:
        form = PolicyAgricultureForm()
    return render(request, 'customer/moredetails_agriculture.html', {'form': form})

def apply_policy_property(request):
    if request.method == 'POST':
        form = PolicyPropertyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_url')  
    else:
        form = PolicyPropertyForm()
    return render(request, 'customer/moredetails_fire.html', {'form': form})

def apply_policy_medical(request):
    if request.method == 'POST':
        form = PolicyMedicalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_url') 
    else:
        form = PolicyMedicalForm()
    return render(request, 'customer/moredetails-medial.html', {'form': form})
