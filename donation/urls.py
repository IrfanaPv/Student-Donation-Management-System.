from django.urls import path
from .import views

urlpatterns=[
      path('',views.home_page,name='home_page'),
      path('login_page',views.login_page,name='login_page'),
      path('login_save',views.login_save,name="login_save"),
      path('help_request',views.help_request,name='help_request'),
      path('save_request',views.save_request,name='save_request'),
      path('register_student',views.register_student,name='register_student'),
      path('save_student',views.save_student,name='save_student'),
      path('student_dashboard',views.student_dashboard,name="student_dashboard"),
      path('register_donor',views.register_donor,name='register_donor'),
      path('save_donor',views.save_donor,name='save_donor'),
      path('donation/', views.donation, name='donation'),
      path('donor_dashboard',views.donor_dashboard,name='donor_dashboard'),
      path('admin_dashboard',views.admin_dashboard,name='admin_dashboard'),
      path('approve_request/<int:id>',views.approve_request,name='approve_request'),
      path('reject_request/<int:id>',views.reject_request,name='reject_request'),
      path('view_donations',views.view_donations,name='view_donations'),
      path('view_requests',views.view_requests,name='view_requests'),
      path('view_sudents',views.view_sudents,name='view_sudents'),
      path('view_donors',views.view_donors, name='view_donors'),
      path('view_pendingrequests',views.view_pendingrequests,name='view_pendingrequests'),
      path('download_report_pdf/', views.download_report_pdf, name='download_report_pdf'),
      path('logout_page',views.logout_page,name='logout_page'),
      path('student_profile',views.student_profile,name='student_profile'),
      path('update_student',views.update_student,name='update_student'),
      path('s_updation<int:id>',views.s_updation,name='s_updation'),
      path('donor_profile',views.donor_profile,name='donor_profile'),
      path('update_donor',views.update_donor,name='update_donor'),
      path('d_updation/<int:id>',views.d_updation,name='d_updation'),
      path('create_order/<int:req_id>/', views.create_order, name='create_order'),
      path('payment_success/', views.payment_success, name='payment_success')




]