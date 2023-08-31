
from django.contrib import admin
from django.urls import path
from insurance import views
from django.contrib.auth.views import LogoutView,LoginView
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('customer/',include('customer.urls')),
    path('',views.home_view,name='home'),
    
    path('logout', LogoutView.as_view(template_name='index.html'),name='logout'),
    path('products', views.products,name='products'),
    path('vignette', views.vignette,name='vignette'),
    path('contactus', views.contactus_view),
    path('afterlogin', views.afterlogin_view,name='afterlogin'),

    path('view_policy', views.view_policy,name='view_policy'),
    path('view_policy_vehicle', views.admin_view_vehicle,name='view_policy_vehicle'),
    path('view_policy_agri', views.admin_view_agri,name='view_policy_agri'),

    path('claim_feedback/<str:email>',views.claimFeedback,name="claim_feedback"),
    path('insurance/report',views.report,name="report"),

    path('renderpdf/<int:id>',views.generate_pdf,name="pdf_view"),

    path('admin-send-vignette/<int:id>',views.adminsendvignette,name="admin-send-vignette"),

    
    path('adminlogin', LoginView.as_view(template_name='insurance/adminlogin.html'),name='adminlogin'),
    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),

    path('admin-view-customer', views.admin_view_customer_view,name='admin-view-customer'),
    path('update-customer/<int:pk>', views.update_customer_view,name='update-customer'),
    path('delete-customer/<int:pk>', views.delete_customer_view,name='delete-customer'),

    path('admin-category', views.admin_category_view,name='admin-category'),
    path('admin-view-category', views.admin_view_category_view,name='admin-view-category'),
    path('admin-update-category', views.admin_update_category_view,name='admin-update-category'),
    path('update-category/<int:pk>', views.update_category_view,name='update-category'),
    path('admin-add-category', views.admin_add_category_view,name='admin-add-category'),
    path('admin-delete-category', views.admin_delete_category_view,name='admin-delete-category'),
    path('delete-category/<int:pk>', views.delete_category_view,name='delete-category'),


    path('admin-policy', views.admin_policy_view,name='admin-policy'),
    path('admin-add-policy', views.admin_add_policy_view,name='admin-add-policy'),
    path('admin-view-policy', views.admin_view_policy_view,name='admin-view-policy'),
    path('admin-update-policy', views.admin_update_policy_view,name='admin-update-policy'),
    path('update-policy/<int:pk>', views.update_policy_view,name='update-policy'),
    path('admin-delete-policy', views.admin_delete_policy_view,name='admin-delete-policy'),
    path('delete-policy/<int:pk>', views.delete_policy_view,name='delete-policy'),

    path('admin-view-policy-holder', views.admin_view_policy_holder_view,name='admin-view-policy-holder'),
    path('admin-view-approved-policy-holder', views.admin_view_approved_policy_holder_view,name='admin-view-approved-policy-holder'),
    path('admin-view-disapproved-policy-holder', views.admin_view_disapproved_policy_holder_view,name='admin-view-disapproved-policy-holder'),
    path('admin-view-waiting-policy-holder', views.admin_view_waiting_policy_holder_view,name='admin-view-waiting-policy-holder'),
    path('approve-request/<int:pk>', views.approve_request_view,name='approve-request'),
    path('reject-request/<int:pk>', views.disapprove_request_view,name='reject-request'),

    path('approve-request-agri/<int:pk>', views.approve_request_view_agri,name='approve-request-agri'),
    path('reject-request-agri/<int:pk>', views.disapprove_request_view_agri,name='reject-request-agri'),

    path('admin-question', views.admin_question_view,name='admin-question'),
    path('admin-claim', views.admin_claim_view,name='admin-claim'),
    path('update-question/<int:pk>', views.update_question_view,name='update-question'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
