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

        # # For Appraisal
        # path('appraisee/', views.AppraiseListView.as_view(), name='appraise_view'),
        # path('appraisee/personal/<int:id>/', views.AppraiseUpdateView.as_view(), name='appraise_personal_update_view'),
        # path('appraisee/posting/<int:id>/', views.AppraiseUpdateViewPosting.as_view(), name='appraise_posting_update_view'),
        # path('appraisee/additional/<int:id>/', views.AppraiseUpdateViewAdditional.as_view(), name='appraise_additional_update_view'),
        # path('appraisee/kpi/<int:id>/', views.AppraiseUpdateViewKpi.as_view(), name='appraise_kpi_update_view'),
        # path('appraisee/question/<int:id>/', views.AppraiseUpdateViewQuestion.as_view(), name='appraise_question_update_view'),
        # path('appraisee/print/<int:id>/', views.AppraiseUpdateViewPrint.as_view(), name='appraise_print_update_view'),

        # # For Reporting
        # path('reporting/', views.ReportingListView.as_view(), name='reporting_view'),
        # path('reporting/preview/<int:id>/', views.ReportingUpdateViewPreview.as_view(), name='reporting_preview_view'),
        # path('reporting/question/<int:id>/', views.ReportingUpdateViewQuestion.as_view(), name='reporting_question_update_view'),
        # path('reporting/kpi/<int:id>/', views.ReportingUpdateViewKpi.as_view(), name='reporting_kpi_update_view'),
        # path('reporting/question2/<int:id>/', views.ReportingUpdateViewQuestion2.as_view(), name='reporting_question2_update_view'),
        # path('reporting/preview2/<int:id>/', views.ReportingUpdateViewPreview2.as_view(), name='reporting_preview2_view'),

        # # For Reporting class3
        # path('reportingclass3/', views.ReportingClass3ListView.as_view(), name='reporting_class_3'),
        # path('reportingclass3/personal/<int:id>/', views.ReportingClass3UpdateView.as_view(), name='reporting_class_3_personal_update_view'),
        # path('reportingclass3/questions/<int:id>/', views.ReportingClass3UpdateViewQuestion.as_view(), name='reporting_class_3_questions_update_view'),
        # path('reportingclass3/print/<int:id>/', views.ReportingClass3ViewPrint.as_view(), name='reporting_class_3_print_view'),

        # # For Reviewing
        # path('reviewing/', views.ReviewingListView.as_view(), name='reviewing_view'),
        # path('reviewing/preview/<int:id>/', views.ReviewingUpdateViewPreview.as_view(), name='reviewing_preview_view'),
        # path('reviewing/question/<int:id>/', views.ReviewingUpdateViewQuestion.as_view(), name='reviewing_question_update_view'),
        # path('reviewing/kpi/<int:id>/', views.ReviewingUpdateViewKpi.as_view(), name='reviewing_kpi_update_view'),
        # path('reviewing/preview2/<int:id>/', views.ReviewingUpdateViewPreview2.as_view(), name='reviewing_preview2_view'),

        # # For Reporting class3
        # path('reviewingclass3/', views.ReviewingClass3ListView.as_view(), name='reviewing_class_3'),
        # path('reviewingclass3/preview/<int:id>/', views.ReviewingClass3ViewPreview.as_view(),name='reviewing_class_3_preview_view'),
        # path('reviewingclass3/questions/<int:id>/', views.ReviewingClass3UpdateViewQuestion.as_view(),name='reviewing_class_3_questions_update_view'),
        # path('reviewingclass3/print/<int:id>/', views.ReviewingClass3ViewPrint.as_view(),name='reviewing_class_3_print_view'),

        # # For Accepting
        # path('accepting/', views.AcceptingListView.as_view(), name='accepting_view'),
        # path('accepting/preview/<int:id>/', views.AcceptingUpdateViewPreview.as_view(), name='accepting_preview_view'),
        # path('accepting/question/<int:id>/', views.AcceptingUpdateViewQuestion.as_view(), name='accepting_question_update_view'),
        # path('accepting/preview2/<int:id>/', views.AcceptingUpdateViewPreview2.as_view(), name='accepting_preview2_view'),

        # # For Reporting class3
        # path('acceptingclass3/', views.AcceptingClass3ListView.as_view(), name='accepting_class_3'),
        # path('acceptingclass3/preview/<int:id>/', views.AcceptingClass3ViewPreview.as_view(),name='accepting_class_3_preview_view'),
        # path('acceptingclass3/questions/<int:id>/', views.AcceptingClass3UpdateViewQuestion.as_view(),name='accepting_class_3_questions_update_view'),
        # path('acceptingclass3/print/<int:id>/', views.AcceptingClass3ViewPrint.as_view(),name='accepting_class_3_print_view'),


        # # Fetch Pdf
        # path('acr/pdf/', views.AcrPdfListView.as_view(), name='acr_pdf_view'),
        # path('acr/forward/<int:taggingId>/', views.AcrForwardReporting.as_view(), name='acr_forward_view'),
        # path('acr/forwardClass3/<int:taggingId>/', views.AcrForwardReportingClass3.as_view(), name='acr_forward_view'),
        # path('acr/forwardReviewing/<int:taggingId>/', views.AcrForwardReviewing.as_view(), name='acr_forward_view'),
        # path('acr/forwardReviewingClass3/<int:taggingId>/', views.AcrForwardReviewingClass3.as_view(), name='acr_forward_view'),

        # Fetch Data From Apis
        path('ajax/load-posting-data/', views.load_posting_data, name='ajax_load_posting_data'),
        path('download-excel/<str:type>/', admin.download_excel, name='download_excel'),
        path('generate_pdf/<str:taggingId>/', views.generate_pdf, name='download_excel'),
        # Extras
        path('reporting_form_hindi/',views.reporting_je_form_hindi,name='reporting_form_hindi'),
        # path('reporting_form_hindi/',views.reporting_ta_form_hindi,name='reporting_form_hindi'),
        path('reporting/', views.ReportingListView, name='reporting_view'),
        path('update_reporting_je_form_hindi/',views.update_reporting_je_form_hindi,name='update_reporting_je_form_hindi'),
        path('reporting_preview/<int:officer_id>/<int:tagging_id>',views.reporting_preview,name='reporting_preview'),
        path('generate_pdf_reporting_officer',views.generate_pdf_reporting_officer,name="generate_pdf_reporting_officer")



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
