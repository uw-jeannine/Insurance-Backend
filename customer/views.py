from django.shortcuts import render,redirect,reverse, HttpResponse
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
from customer.models import Customer,ApplyPolicyVehicle, Submit_claim,ApplyPolicyAgriculture
from django.contrib import messages
from insurance.models import Policy,Category, PolicyRecord
import random
from django.contrib import messages



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
    record = PolicyRecord.objects.filter(customer__user=request.user).count()
    customer = Customer.objects.get(user_id=request.user.id)
    print(customer.profile_pic)
    # print(record)
    dict={
        'customer':customer,
        'available_policy':CMODEL.Policy.objects.all().count(),
        'applied_policy':record,
        'total_category':Category.objects.all().count(),
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
    policies = PolicyRecord.objects.filter(customer=customer).all()
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
    customer = models.Customer.objects.get(user_id=request.user.id)
    if request.method == 'POST':
        submit_claim = Submit_claim()
        submit_claim.name =  request.POST['name']
        submit_claim.email = request.POST['email']
        submit_claim.phonenumber = request.POST['phonenumber']
        submit_claim.claim_type = request.POST['claimtype'] 
        submit_claim.description = request.POST['description']
        submit_claim.dateofincident = request.POST['dateofincident']
        submit_claim.location = request.POST['location']
        submit_claim.witnessinformation = request.POST['witnessinformation']
        submit_claim.vehicleproperty =  request.POST['vehicleproperty']
        submit_claim.policereport =  request.FILES['policereport'] 
        submit_claim.injuryinformation = request.POST['injuryinformation']
        submit_claim.uploadphotos = request.FILES['uploadphotos']
        submit_claim.additionalcomment = request.POST['additionalcomment']
        submit_claim.coverage_amount = request.POST['coverage_amount']
        submit_claim.save()
        messages.success( request,"Claims added successfully")
    context = {"customer": customer}
    return render(request,'customer/submit_claim.html', context=context)

def claim_history_view(request):
    return render(request,'customer/claim_history.html')


def moredetail_vehicle(request,id):
    years = list(range(1950, 2023))
    getrecord = Policy.objects.get(id=id)
    print(getrecord.id)
    if request.method == 'POST':
        applyData =  ApplyPolicyVehicle()
        applyData.marque =  request.POST['marque']
        applyData.platenumnber = request.POST['platenumber']
        applyData.yearofmanufacture =  request.POST['yearofmanufacture']
        applyData.insuredvalue =  request.POST['insuredvalue']
        applyData.territoriallimit = request.POST['territoriallimit']
        applyData.model = request.POST['model']
        applyData.numberofchasis = request.POST['numberofchasis']
        applyData.seatcapacity = request.POST['seatcapacity']
        applyData.occupantcover = request.POST['occupantcovered']
        applyData.policystatus = 'Pending'
        applyData.customerid = models.Customer.objects.get(user_id=request.user.id)
        policy_instance = Policy.objects.get(id=id)
        applyData.applyid = policy_instance
        trk = random.randint(1,9999999)
        applyData.tracking_number = trk
        applyData.save()
        messages.success(request,'Your application sent successfully'+str(trk)+'this is tracking number')
        return render(request,'customer/history.html',{'trk':trk,'status':'Pending'})
    return render(request,'customer/moredetail-vehicle.html',{'id':getrecord.id,'years':years})

        

def moredetail_medical(request):
    userForm=forms.CustomerUserForm()
    customerForm=forms.CustomerForm()
    mydict={'userForm':userForm,'customerForm':customerForm}
    return render(request,'customer/moredetails-medical.html',context=mydict)


def moredetail_fire(request):
    userForm=forms.CustomerUserForm()
    customerForm=forms.CustomerForm()
    mydict={'userForm':userForm,'customerForm':customerForm}
    return render(request,'customer/moredetails_fire.html',context=mydict)


def moredetail_agriculture(request,id):
    userForm=forms.CustomerUserForm()
    customerForm=forms.CustomerForm()

    if request.method == 'POST':
        agri = ApplyPolicyAgriculture()
        agri.policy_status = 'Pending'
        agri.location = request.POST.get('location')
        agri.insurance_type = request.POST.get('insurancetype')
        agri.crop_name = request.POST.get('cropname')
        agri.crop_type = request.POST.get('croptype')
        agri.planting_date = request.POST.get('plantingdate')
        agri.harvest_date = request.POST.get('harvestdate')
        agri.plot_size = request.POST.get('plotsize')
        agri.soiltype = request.POST.get('soiltype')
        agri.customerid = models.Customer.objects.get(user_id=request.user.id)
        policy_instance = Policy.objects.get(id=id)
        agri.appliedid = policy_instance
        trk = random.randint(1,9999999)
        agri.tracking_number = trk
        agri.save()
        return render(request,'customer/history.html',{'trk':trk,'status':'Pending'})



    mydict={'userForm':userForm,'customerForm':customerForm}
    return render(request,'customer/moredetails_agriculture.html',context=mydict)


# def apply_policy_agriculture(request):
#     if request.method == 'POST':
#         form = PolicyAgricultureForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('success_url')  
#     else:
#         form = PolicyAgricultureForm()
#     return render(request, 'customer/moredetails_agriculture.html', {'form': form})

# def apply_policy_property(request):
#     if request.method == 'POST':
#         form = PolicyPropertyForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('success_url')  
#     else:
#         form = PolicyPropertyForm()
#     return render(request, 'customer/moredetails_fire.html', {'form': form})

# def apply_policy_medical(request):
#     if request.method == 'POST':
#         form = PolicyMedicalForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('success_url') 
#     else:
#         form = PolicyMedicalForm()
#     return render(request, 'customer/moredetails-medial.html', {'form': form})


def tracking(request):
    if request.method == 'POST':
        getdata =  request.POST.get('type')
        trackingnumber = request.POST.get('tnumber')
        if getdata == 'car':
            records = ApplyPolicyVehicle.objects.filter(tracking_number=trackingnumber).all()
            return render(request, 'customer/tracking_number.html', {'records': records})
        elif getdata == 'agri':
            recordsagri = ApplyPolicyAgriculture.objects.filter(tracking_number=trackingnumber).all()
            return render(request, 'customer/tracking_number.html', {'recordsagri': recordsagri})
        return render(request, 'customer/tracking_number.html')

  
    return render(request,'customer/tracking_number.html')


def detailapply(request,id):
    recordselect = Policy.objects.get(id=id)
    category = recordselect.category.category_name
    years = list(range(1950, 2023))
    print(category)
    
    if category == 'Vehicle insurance':
        # Render the motor category form
        return render(request, 'customer/moredetail-vehicle.html', context={"years": years, "policy": recordselect})
    elif category == 'Agriculture insurance':

        # Render the agriculture category form
        return render(request, 'customer/moredetails_agriculture.html', {'policy': recordselect})
    elif category == 'Medical insurance':
        # Render the medical category form
        return render(request, 'customer/moredetails-medical.html', {'policy': recordselect})
    elif category == 'Fire insurance':
        # Render the fire category form
        return render(request, 'customer/moredetails_fire.html', {'policy': recordselect})
    else:
        # Handle the case where the category is not recognized
        return HttpResponse("Invalid policy category")
    
    
import requests
import json
from paypack.transactions import Transaction
from paypack.client import HttpClient
# from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_exempt

def paypack(request):

    from paypack.client import HttpClient

    client_id="0e703f9e-5b76-11ee-86e8-deaddb65b9c2"
    client_secret="b242a7e48b1b03d5a83176aa3b3c4742da39a3ee5e6b4b0d3255bfef95601890afd80709"

    HttpClient(client_id=client_id, client_secret=client_secret)


    cashin = Transaction().cashin(amount=100, phone_number="0786004321", mode="development")
    print(cashin)
   
    return HttpResponse('Success')


@csrf_exempt
def paypack1(request):
    body = json.loads(request.body)
    if request.method == 'POST' and body['data']['status'] =='successful':



        print(body)

    return HttpResponse('Success')