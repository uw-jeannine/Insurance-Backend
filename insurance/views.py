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
from django.contrib.auth.models import User
from customer import models as CMODEL
from customer import forms as CFORM
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail,EmailMessage
from django.conf import settings
from django.contrib import messages
from customer.models import ApplyPolicyAgriculture,ApplyPolicyVehicle,ApplyPolicyMedical
from django.template.loader import get_template
from customer.models import Customer

import datetime


from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from dateutil.relativedelta import relativedelta

def generate_pdf(request,id):
    # Render the HTML template
    
    records = CMODEL.ApplyPolicyVehicle.objects.get(id=id)
    user_instance = get_object_or_404(User,id = records.applyid.id)
    recordscustomer = models.Policy.objects.get(id=user_instance.id)
    print(user_instance)
    current_date = datetime.date.today()
    months_to_add = recordscustomer.tenure
    new_date = current_date + relativedelta(months=months_to_add)
    print(new_date)

    data = {
        'image': 'static/images/images.png',
        'today': datetime.date.today(), 
        'expire':new_date
        }
    print(recordscustomer.tenure)

    html = render_to_string('insurance/pdfs/invoice.html', {'data': records,'date':data})

    # Create a PDF object
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="generated_pdf.pdf"'

    # Generate PDF using xhtml2pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF', content_type='text/plain')

    return response

def adminsendvignette(request,id):
    policyrecords = CMODEL.ApplyPolicyVehicle.objects.get(id=id)
    user_instance = get_object_or_404(User, id=policyrecords.customerid.id)

    recordscustomer = CMODEL.Customer.objects.get(id=user_instance.id)
    print(recordscustomer.email)
    if request.method == 'POST':
        subject = 'Reply Claim feedback'
        attachment_data = request.FILES.get('sendvignette')
        print(attachment_data)
        message = str('Send Vignette')
        html_message = str('Send Vignette')
        from_email =   settings.EMAIL_HOST_USER
        recipient_list = [str(recordscustomer.email)]
        email = EmailMessage(
            subject, 
            message, 
            from_email, 
            recipient_list,



            
            )
        email.attach(
            attachment_data.name,
            attachment_data.read(),
            attachment_data.content_type
        )
        email.send()
        messages.success( request,"Vignette sent successfully")
    return render(request,'insurance/send_vegnite.html',{'id':id})


def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')  
    return render(request,'index.html')


def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()


def afterlogin_view(request):
    if is_customer(request.user):      
        return redirect('customer/customer-dashboard')
    else:
        return redirect('admin-dashboard')



def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    customers = Customer.objects.all()
    dict={
        'total_user':CMODEL.Customer.objects.all().count(),
        'total_policy':models.Policy.objects.all().count(),
        'total_category':models.Category.objects.all().count(),
        'total_question':models.Question.objects.all().count(),
        'total_policy_holder':models.PolicyRecord.objects.all().count(),
        'approved_policy_holder':models.PolicyRecord.objects.all().filter(status='Approved').count(),
        'disapproved_policy_holder':models.PolicyRecord.objects.all().filter(status='Disapproved').count(),
        'waiting_policy_holder':models.PolicyRecord.objects.all().filter(status='Pending').count(),
        'customers':customers
    }
    return render(request,'insurance/admin_dashboard.html',context=dict)



@login_required(login_url='adminlogin')
def admin_view_customer_view(request):
    customers= CMODEL.Customer.objects.all()
    return render(request,'insurance/admin_view_customer.html',{'customers':customers})

@login_required(login_url='adminlogin')
def update_customer_view(request,pk):
    customer=CMODEL.Customer.objects.get(id=pk)
    user=CMODEL.User.objects.get(id=customer.user_id)
    userForm=CFORM.CustomerUserForm(instance=user)
    customerForm=CFORM.CustomerForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=CFORM.CustomerUserForm(request.POST,instance=user)
        customerForm=CFORM.CustomerForm(request.POST,request.FILES,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return redirect('admin-view-customer')
    return render(request,'insurance/update_customer.html',context=mydict)



@login_required(login_url='adminlogin')
def delete_customer_view(request,pk):
    customer=CMODEL.Customer.objects.get(id=pk)
    user=User.objects.get(id=customer.user_id)
    user.delete()
    customer.delete()
    return HttpResponseRedirect('/admin-view-customer')



def admin_category_view(request):
    return render(request,'insurance/admin_category.html')

def admin_add_category_view(request):
    categoryForm=forms.CategoryForm() 
    if request.method=='POST':
        categoryForm=forms.CategoryForm(request.POST)
        if categoryForm.is_valid():
            categoryForm.save()
            return redirect('admin-view-category')
    return render(request,'insurance/admin_add_category.html',{'categoryForm':categoryForm})

def admin_view_category_view(request):
    categories = models.Category.objects.all()
    return render(request,'insurance/admin_view_category.html',{'categories':categories})

def admin_delete_category_view(request):
    categories = models.Category.objects.all()
    return render(request,'insurance/admin_delete_category.html',{'categories':categories})
    
def delete_category_view(request,pk):
    category = models.Category.objects.get(id=pk)
    category.delete()
    return redirect('admin-delete-category')

def admin_update_category_view(request):
    categories = models.Category.objects.all()
    return render(request,'insurance/admin_update_category.html',{'categories':categories})

@login_required(login_url='adminlogin')
def update_category_view(request,pk):
    category = models.Category.objects.get(id=pk)
    categoryForm=forms.CategoryForm(instance=category)
    
    if request.method=='POST':
        categoryForm=forms.CategoryForm(request.POST,instance=category)
        
        if categoryForm.is_valid():

            categoryForm.save()
            return redirect('admin-update-category')
    return render(request,'insurance/update_category.html',{'categoryForm':categoryForm})
  
  

def admin_policy_view(request):
     dict={
        'total_policy_holder':models.Category.objects.all().count(),
        'approved_policy_holder':models.PolicyRecord.objects.all().filter(status='Approved').count(),
        'disapproved_policy_holder':models.PolicyRecord.objects.all().filter(status='Disapproved').count(),
        'waiting_policy_holder':models.PolicyRecord.objects.all().filter(status='Pending').count(),
    }
     return render(request,'insurance/admin_policy.html',context=dict)


def admin_add_policy_view(request):
    policyForm=forms.PolicyForm() 
    if request.method=='POST':
        policyForm=forms.PolicyForm(request.POST)
        if policyForm.is_valid():
            categoryid = request.POST.get('category')
            category = models.Category.objects.get(id=categoryid) 
            policy = policyForm.save(commit=False)
            policy.category=category
            policy.save()
            return redirect('admin-view-policy')
    return render(request,'insurance/admin_add_policy.html',{'policyForm':policyForm})

def admin_view_policy_view(request):
    policies = models.Policy.objects.all()
    print(policies)
    return render(request,'insurance/admin_view_policy.html',{'policies':policies})



def admin_update_policy_view(request):
    policies = models.Policy.objects.all()
    return render(request,'insurance/admin_update_policy.html',{'policies':policies})

@login_required(login_url='adminlogin')
def update_policy_view(request,pk):
    policy = models.Policy.objects.get(id=pk)
    policyForm=forms.PolicyForm(instance=policy)
    
    if request.method=='POST':
        policyForm=forms.PolicyForm(request.POST,instance=policy)
        
        if policyForm.is_valid():

            categoryid = request.POST.get('category')
            category = models.Category.objects.get(id=categoryid)
            
            policy = policyForm.save(commit=False)
            policy.category=category
            policy.save()
           
            return redirect('admin-update-policy')
    return render(request,'insurance/update_policy.html',{'policyForm':policyForm})
  
  
def admin_delete_policy_view(request):
    policies = models.Policy.objects.all()
    return render(request,'insurance/admin_delete_policy.html',{'policies':policies})
    

def claimFeedback(request,email):
    if request.method == 'POST':
        subject = 'Insurance Claim feedback'
        message = request.POST.get('message')
        html_message = str(message)
        from_email =   settings.EMAIL_HOST_USER
        recipient_list = [str(email)]
        send_mail(subject, message, from_email, recipient_list, html_message=html_message)
        messages.success( request,"Claims added successfully")
    return render(request,'insurance/claimfeedback.html',{'email': email})



def report(request):
    records = CMODEL.ApplyPolicyVehicle.objects.all()
    customers = CMODEL.Customer.objects.all()
    policy = models.Policy.objects.all()
    

    

    html = render_to_string('insurance/pdfs/report.html', {
        'datas': customers,
        'datasapl':records,
        'datasap':policy

    })

    # Create a PDF object
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="generated_pdf.pdf"'

    # Generate PDF using xhtml2pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF', content_type='text/plain')

    return response


def delete_policy_view(request,pk):
    policy = models.Policy.objects.get(id=pk)
    policy.delete()
    return redirect('admin-delete-policy')

def admin_view_policy_holder_view(request):
    policyrecords = models.PolicyRecord.objects.all()
    return render(request,'insurance/admin_view_policy_holder.html',{'policyrecords':policyrecords})

def admin_view_approved_policy_holder_view(request):
    policyrecords = models.PolicyRecord.objects.all().filter(status='Approved')
    return render(request,'insurance/admin_view_approved_policy_holder.html',{'policyrecords':policyrecords})

def admin_view_disapproved_policy_holder_view(request):
    policyrecords = models.PolicyRecord.objects.all().filter(status='Disapproved')
    return render(request,'insurance/admin_view_disapproved_policy_holder.html',{'policyrecords':policyrecords})

def admin_view_waiting_policy_holder_view(request):
    policyrecords = models.PolicyRecord.objects.all().filter(status='Pending')
    return render(request,'insurance/admin_view_waiting_policy_holder.html',{'policyrecords':policyrecords})

def approve_request_view(request,pk):
    policyrecords = CMODEL.ApplyPolicyVehicle.objects.get(id=pk)
    user_instance = get_object_or_404(User,id = policyrecords.customerid.id)
    recordscustomer = CMODEL.Customer.objects.get(id=user_instance.id)
    print(recordscustomer.email)
    subject = 'Insurance application'
    message = 'This Auto Insurance System. we wanted to let you know that your application was received and has been approved'
    html_message = '<p>To procceed, you will need to make <strong>Payment</strong> through this contact.</p> <p>Contact: 0786004321</p> or <p>Bank account: 40019003828</p> <p> For more information do not hestitate to contact us </p>'
    from_email =   settings.EMAIL_HOST_USER
    recipient_list = [str(recordscustomer.email)]
    send_mail(subject, message, from_email, recipient_list, html_message=html_message)
    policyrecords.policystatus='Approved'
    policyrecords.save()
    return redirect('view_policy_vehicle')

def disapprove_request_view(request,pk):
    policyrecords = CMODEL.ApplyPolicyVehicle.objects.get(id=pk)
    user_instance = get_object_or_404(User,id = policyrecords.customerid.id)
    recordscustomer = CMODEL.Customer.objects.get(id=user_instance.id)
    print(recordscustomer.email)
    subject = 'Insurance application'
    message = 'This is Auto Insurance System. we wanted to let you know that your application was received and has been disapproved.'
    html_message = '<p> Contact us For more clarification. </p> <p>Contact: 0786004321</p>'
    from_email =   settings.EMAIL_HOST_USER
    recipient_list = [str(recordscustomer.email)]
    send_mail(subject, message, from_email, recipient_list, html_message=html_message)
    policyrecords.policystatus='Disapproved'
    policyrecords.save()
    return redirect('view_policy_vehicle')

def view_policy(request):
    dict={
        'total_applied_vehicle':CMODEL.ApplyPolicyVehicle.objects.all().count(),
        'total_applied_agri':CMODEL.ApplyPolicyAgriculture.objects.all().count()  
    }
    return render(request,'insurance/view_policy.html',dict)

def admin_view_vehicle(request):
    record = CMODEL.ApplyPolicyVehicle.objects.all()
    return render(request,'insurance/admin_view_vehicle.html',{"datas":record})

def admin_view_agri(request):
    record = CMODEL.ApplyPolicyAgriculture.objects.all()
    return render(request,'insurance/admin_view_agri.html',{"datas":record})


def approve_request_view_agri(request,pk):
    policyrecords = CMODEL.ApplyPolicyAgriculture.objects.get(id=pk)
    user_instance = get_object_or_404(User,id = policyrecords.customerid.id)
    recordscustomer = CMODEL.Customer.objects.get(id=user_instance.id)
    print(recordscustomer.email)
    subject = 'Insurance application'
    message = 'This Auto Insurance System. we wanted to let you know that your application was received and has been approved'
    html_message = '<p>To procceed, you will need to make <strong>Payment</strong> through this contact.</p> <p>Contact: 0786004321</p> or <p>Bank account: 40019003828</p> <p> For more information do not hestitate to contact us </p>'
    from_email =   settings.EMAIL_HOST_USER
    recipient_list = [str(recordscustomer.email)]
    send_mail(subject, message, from_email, recipient_list, html_message=html_message)

    policyrecords.policy_status='Approved'
    policyrecords.save()
    return redirect('view_policy_agri')

def disapprove_request_view_agri(request,pk):
    policyrecords = CMODEL.ApplyPolicyAgriculture.objects.get(id=pk)
    user_instance = get_object_or_404(User,id = policyrecords.customerid.id)
    recordscustomer = CMODEL.Customer.objects.get(id=user_instance.id)
    print(recordscustomer.email)
    subject = 'Insurance application'
    message = 'This is Auto Insurance System. we wanted to let you know that your application was received and has been disapproved.'
    html_message = '<p> Contact us For more clarification. </p> <p>Contact: 0786004321</p>'+message
    from_email =   settings.EMAIL_HOST_USER
    recipient_list = [str(recordscustomer.email)]
    send_mail(subject, message, from_email, recipient_list, html_message=html_message)
    policyrecords.policy_status='Disapproved'
    policyrecords.save()
    return redirect('view_policy_agri')


def admin_question_view(request):
    questions = models.Question.objects.all()
    return render(request,'insurance/admin_question.html',{'questions':questions})

def admin_claim_view(request):
    questions = CMODEL.Submit_claim.objects.all()
    return render(request,'insurance/admin_claims.html',{'claims':questions})

def update_question_view(request,pk):
    question = models.Question.objects.get(id=pk)
    questionForm=forms.QuestionForm(instance=question)
    
    if request.method=='POST':
        questionForm=forms.QuestionForm(request.POST,instance=question)
        
        if questionForm.is_valid():

            admin_comment = request.POST.get('admin_comment')
            
            
            question = questionForm.save(commit=False)
            question.admin_comment=admin_comment
            question.save()
           
            return redirect('admin-question')
    return render(request,'insurance/update_question.html',{'questionForm':questionForm})

def aboutus_view(request):
    return render(request,'insurance/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'insurance/contactussuccess.html')
    return render(request, 'insurance/contactus.html', {'form':sub})



def vignette(request):
    return render(request,'vignette.html')

def products(request):
    return render(request,'products.html')

