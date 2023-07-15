from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.index_home,name='index_home'),
    path('customerclick', views.customerclick_view,name='customerclick'),
    path('customersignup', views.customer_signup_view,name='customersignup'),
    path('customer-dashboard', views.customer_dashboard_view,name='customer-dashboard'),
    path('customerlogin', LoginView.as_view(template_name='insurance/adminlogin.html'),name='customerlogin'),

    path('apply-policy', views.apply_policy_view,name='apply-policy'),
    path('apply/<int:pk>', views.apply_view,name='apply'),
    path('history', views.history_view,name='history'),

    path('ask-question', views.ask_question_view,name='ask-question'),
    path('question-history', views.question_history_view,name='question-history'),

    path('moredetail-vehicle', views.moredetail_vehicle,name='moredetail-vehicle'),
    path('moredetail-medical', views.moredetail_medical,name='moredetail-medical'),
    path('moredetail-life', views.moredetail_life,name='moredetail-life'),
    path('moredetail-travel', views.moredetail_travel,name='moredetail-travel'),

]