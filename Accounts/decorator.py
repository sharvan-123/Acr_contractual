from .models import ACR_Dates, ACR_Session
from django.contrib import messages
from django.shortcuts import redirect
from datetime import datetime

def check_valid_referer(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.META.get('HTTP_REFERER'):
            return redirect('Dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

def check_valid_dates(Type):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            # Session = ACR_Session.objects.filter(isActive=True)[0]  # Assumes you have at least one instance of MyModel
            # Date = ACR_Dates.objects.filter(acr_session=Session)[0]
            # if Type == 'Tagging':
            #     if request.user.employmentType['empTypeId'] not in [6]:
            #         messages.error(request, 'You are not authorized to perform this task.')
            #         return redirect('Dashboard')
            #     elif Date.tagging_start_date <= datetime.now().date() <= Date.tagging_end_date:
            #         return view_func(request, *args, **kwargs)
            #     else:
            #         messages.error(request, 'Filling of Tagging Form is allowed from ' + str(
            #             Date.tagging_start_date) + ' to ' + str(Date.tagging_end_date))
            #         return redirect('Dashboard')
            # if Type == 'Appraisee':
            #     if EmployeeSelfAppraisal.objects.filter(taggingId=kwargs['id']).exists():
            #         if EmployeeSelfAppraisal.objects.get(taggingId=kwargs['id']).isStatus:
            #             messages.error(request, 'You ACR for this Session has already been submitted.')
            #             return redirect('appraise_view')
            #     if request.user.employmentType['empTypeId'] not in [1,5,7,9]:
            #         messages.error(request, 'You are not authorized to perform this task.')
            #         return redirect('appraise_view')
            #     elif request.user.designation['designationClass'] not in ["1", "2", "3"]:
            #         messages.error(request, 'You are not authorized to perform this task.')
            #         return redirect('appraise_view')
            #     elif request.user.designation['designationClass'] == "3" and request.user.designation['designationId'] not in [23, 99, 102] :
            #         messages.error(request, 'You are not authorized to perform this task.')
            #         return redirect('appraise_view')
            #     elif Date.appraise_start_date <= datetime.now().date() <= Date.appraise_end_date:
            #         return view_func(request, *args, **kwargs)
            #     else:
            #         messages.error(request, 'Filling of Appraisal Form is allowed from ' + str(
            #             Date.appraise_start_date) + ' to ' + str(Date.appraise_end_date))
            #         return redirect('appraise_view')
            # if Type == 'ReportingClass3':
            #     if EmployeeReportingClass3.objects.filter(taggingId=kwargs['id']).exists():
            #         if EmployeeReportingClass3.objects.get(taggingId=kwargs['id']).isStatus:
            #             messages.error(request, 'Reporting Remarks has already been submitted.')
            #             return redirect('reporting_class_3')
            #     if Date.reporting_start_date <= datetime.now().date() <= Date.reporting_end_date:
            #         return view_func(request, *args, **kwargs)
            #     else:
            #         messages.error(request, 'Filling of Reporting Form is allowed from ' + str(
            #             Date.appraise_start_date) + ' to ' + str(Date.appraise_end_date))
            #         return redirect('reporting_class_3')
            # if Type == 'Reporting':
            #     if EmployeeReporting.objects.filter(taggingId=kwargs['id']).exists():
            #         if EmployeeReporting.objects.get(taggingId=kwargs['id']).isStatus:
            #             messages.error(request, 'Reporting Remarks has already been submitted.')
            #             return redirect('reporting_view')
            #     if Date.reporting_start_date <= datetime.now().date() <= Date.reporting_end_date:
            #         return view_func(request, *args, **kwargs)
            #     else:
            #         messages.error(request, 'Filling of Reporting Form is allowed from ' + str(
            #             Date.reporting_start_date) + ' to ' + str(Date.reporting_end_date))
            #         return redirect('reporting_view')
            # if Type == 'Reviewing':
            #     if EmployeeReviewing.objects.filter(taggingId=kwargs['id']).exists():
            #         if EmployeeReviewing.objects.get(taggingId=kwargs['id']).isStatus:
            #             messages.error(request, 'Reviewing Remarks has already been submitted.')
            #             return redirect('reviewing_view')
            #     if Date.reviewing_start_date <= datetime.now().date() <= Date.reviewing_end_date:
            #         return view_func(request, *args, **kwargs)
            #     else:
            #         messages.error(request, 'Filling of Reporting Form is allowed from ' + str(
            #             Date.reviewing_start_date) + ' to ' + str(Date.reviewing_end_date))
            #         return redirect('reviewing_view')
            # if Type == 'ReviewingClass3':
            #     if EmployeeReportingClass3.objects.filter(taggingId=kwargs['id']).exists():pass
            #     else:
            #         messages.error(request, 'Reporting Remarks has been not submitted.')
            #         return redirect('accepting_class_3')
            #     if EmployeeReviewingClass3.objects.filter(taggingId=kwargs['id']).exists():
            #         if EmployeeReviewingClass3.objects.get(taggingId=kwargs['id']).isStatus:
            #             messages.error(request, 'Reviewing Remarks has already been submitted.')
            #             return redirect('reviewing_view')
            #     if Date.reviewing_start_date <= datetime.now().date() <= Date.reviewing_end_date:
            #         return view_func(request, *args, **kwargs)
            #     else:
            #         messages.error(request, 'Filling of Reporting Form is allowed from ' + str(
            #             Date.reviewing_start_date) + ' to ' + str(Date.reviewing_end_date))
            #         return redirect('reviewing_view')
            # if Type == 'Accepting':
            #     if EmployeeAccepting.objects.filter(taggingId=kwargs['id']).exists():
            #         if EmployeeAccepting.objects.get(taggingId=kwargs['id']).isStatus:
            #             messages.error(request, 'Accepting Remarks has already been submitted.')
            #             return redirect('accepting_view')
            #     if Date.accepting_start_date <= datetime.now().date() <= Date.accepting_end_date:
            #         return view_func(request, *args, **kwargs)
            #     else:
            #         messages.error(request, 'Filling of Reporting Form is allowed from ' + str(
            #             Date.accepting_start_date) + ' to ' + str(Date.accepting_end_date))
            #         return redirect('accepting_view')
            # if Type == 'AcceptingClass3':
            #     if EmployeeReviewingClass3.objects.filter(taggingId=kwargs['id']).exists():pass
            #     else:
            #         messages.error(request, 'Reviewing Remarks has been not submitted.')
            #         return redirect('accepting_class_3')
            #     if EmployeeAcceptingClass3.objects.filter(taggingId=kwargs['id']).exists():
            #         if EmployeeAcceptingClass3.objects.get(taggingId=kwargs['id']).isStatus:
            #             messages.error(request, 'Accepting Remarks has already been submitted.')
            #             return redirect('accepting_class_3')
            #     if Date.accepting_start_date <= datetime.now().date() <= Date.accepting_end_date:
            #         return view_func(request, *args, **kwargs)
            #     else:
            #         messages.error(request, 'Filling of Reporting Form is allowed from ' + str(
            #             Date.accepting_start_date) + ' to ' + str(Date.accepting_end_date))
            #         return redirect('accepting_class_3')
            if Type == 'Tagging':
                return view_func(request, *args, **kwargs)


            return redirect('Dashboard')
        return wrapper
    return decorator
