from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.index_home,name='index_home'),
   
    path('customerclick', views.customerclick_view,name='customerclick'),
    path('customersignup', views.customer_signup_view,name='customersignup'),
    path('customer-dashboard', views.customer_dashboard_view,name='customer-dashboard'),
    path('customerlogin', LoginView.as_view(template_name='insurance/adminlogin.html'),name='customerlogin'),
    path('customer/tracking_number',views.tracking,name='tracking_number'),

    path('apply-policy', views.apply_policy_view,name='apply-policy'),
    path('apply/<str:pk>', views.apply_view,name='apply'),
    path('history', views.history_view,name='history'),

    path('ask-question', views.ask_question_view,name='ask-question'),
    path('question-history', views.question_history_view,name='question-history'),

     path('submit-claim', views.submit_claim_view,name='submit-claim'),
    path('claim-history', views.claim_history_view,name='claim-history'),

    path('moredetail-vehicle/<int:id>', views.moredetail_vehicle,name='moredetail-vehicle'),
    path('moredetail-medical', views.moredetail_medical,name='moredetail-medical'),
    path('moredetail-fire', views.moredetail_fire,name='moredetail-fire'),
    path('moredetail-agriculture/<int:id>', views.moredetail_agriculture,name='moredetail-agriculture'),

    path('detailapply/<int:id>',views.detailapply,name='detailapply'),

    path('paypack/',views.paypack,name='paypack'),
    path('paypack1/',views.paypack1,name='paypack1'),

]
