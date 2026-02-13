from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views, admin
from django.urls import path

urlpatterns = [
        path('', views.dashboard, name='Dashboard'),
        path('forget/password/', views.forgetPassword, name='forget_password'),
        path('sendotp/', views.generate_totp, name='sendotp'),
        # path('send-otp/<int:id>/', views.OTPView.as_view(), name='send_otp'),
        path('login/', views.Login, name='login'),
        path('logout/', views.logout_view, name='logout'),

        # For Taginng
        path('tagging/', views.TaggingCreateView.as_view(), name='tagging_add'),
        path('mis/', views.TaggingListView.as_view(), name='tagging_view'),
        path('mis/<int:pk>/<str:type>/', views.TaggingUpdateView.as_view()),
        path('ajax/load-posting-data/', views.load_posting_data, name='ajax_load_posting_data'),
        path('download-excel/<str:type>/', admin.download_excel, name='download_excel'),
        path('generate_pdf/<str:taggingId>/', views.generate_pdf, name='download_excel'),
        path('emp_tagging_form_je',views.emp_tagging_form_je,name='emp_tagging_form_je'),
        # Extras
        path('reporting_je_form_hindi/',views.reporting_je_form_hindi,name='reporting_je_form_hindi'),
        path('reporting_ta_form_hindi/',views.reporting_ta_form_hindi,name='reporting_ta_form_hindi'),
        path('reporting/', views.ReportingListView, name='reporting_view'),
        path('update_reporting_je_form_hindi/',views.update_reporting_je_form_hindi,name='update_reporting_je_form_hindi'),
        path('update_reporting_ta_form_hindi/',views.update_reporting_ta_form_hindi,name='update_reporting_ta_form_hindi'),
        path('reporting_preview/<int:officer_id>/<int:tagging_id>',views.reporting_preview,name='reporting_preview'),
        path('reporting_ta_preview/<int:officer_id>/<int:tagging_id>',views.reporting_ta_preview,name='reporting_ta_preview'),
        path('generate_pdf_reporting_officer',views.generate_pdf_reporting_officer,name="generate_pdf_reporting_officer"),
        #ReviewvingListView
        path('reviewingList',views.ReviewingListView,name="ReviewingListView"),
        path('reviewingOfficer_form/<int:tagging_id>',views.reviewingOfficer_form,name="reviewingOfficer_form"),
        path('reviewing_preview/<int:tagging_id>',views.reviewing_preview,name='reviewing_preview'),
        path('update_reviewing_form_hindi/<int:tagging_id>',views.update_reviewing_form_hindi,name="update_reviewing_form_hindi"),
        path('generate_pdf_reviewing_officer',views.generate_pdf_reviewing_officer,name="generate_pdf_reviewing_officer"),
        # AcceptingOfficer.........
        path('acceptingListView',views.AcceptingListView,name="AcceptingListView"),
        path('acceptingOfficer_form/<int:tagging_id>',views.acceptingOfficer_form,name="acceptingOfficer_form"),
        path('accepting_preview/<int:tagging_id>',views.accepting_preview,name="accepting_preview"),
        path('update_accepting_form_hindi/<int:tagging_id>',views.update_accepting_form_hindi,name="update_accepting_form_hindi"),
        path('generate_pdf_accepting_officer',views.generate_pdf_accepting_officer,name="generate_pdf_accepting_officer"),
        path('emp_tagging_form_ta',views.emp_tagging_form_ta,name="emp_tagging_form_ta"),
        #for complete acr.........
        path('complete_acr_list',views.complete_acr_list,name="complete_acr_list"),
        #extra 
        path('add_update_emp_profile/', views.update_emp_detail_by_empCode, name='add_update_emp_profile')


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)