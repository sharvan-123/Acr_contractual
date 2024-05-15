from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django_ratelimit.decorators import ratelimit
from dateutil.relativedelta import relativedelta
from django.core.files.base import ContentFile
from django.shortcuts import render
from django.contrib.auth.models import Group
from excel_response import ExcelResponse
from django.urls import reverse_lazy
from django.views import View
from .decorator import *
from .models import *
from .forms import *
from .smsapi import *
import requests
import pdfkit
import pyotp
import json


apiUrl = settings.APIURL

@login_required(login_url='/login/')
def dashboard(request):
    return render(request, 'index.html')


@method_decorator(check_valid_referer, name='dispatch')
@method_decorator(login_required(login_url='/login/'), name='dispatch')
@method_decorator(check_valid_dates('Tagging'), name='dispatch')
class TaggingCreateView(CreateView):
    model = EmployeeTagging
    form_class = EmployeeTaggingForm
    context_object_name = 'tagging_add'
    success_url = reverse_lazy('tagging_add')
    def form_valid(self, form):
        if self.model.objects.filter(
                empCode=form.cleaned_data['empCode'] if form.cleaned_data['empCode'] else self.request.user).filter(
                financialYear=form.cleaned_data['financialYear']).exists():
            messages.error(self.request, 'Tagging for this session has already been submitted.')
            response = super().form_invalid(form)
            return response
        employeeTagging = form.save(commit=False)
        employeeTagging.empCode = form.cleaned_data['empCode'] if form.cleaned_data['empCode'] else self.request.user
        if employeeTagging.isAnotherTagging:
            isAnotherTagging = EmployeeTagging(
                empCode=form.cleaned_data['empCode'] if form.cleaned_data['empCode'] else self.request.user,
                fromDate=form.cleaned_data['fromDate2'],
                toDate=form.cleaned_data['toDate2'],
                region=form.cleaned_data['region2'],
                region_code=form.cleaned_data['region_code2'],
                circle=form.cleaned_data['circle2'],
                circle_code=form.cleaned_data['circle_code2'],
                division=form.cleaned_data['division2'],
                division_code=form.cleaned_data['division_code2'],
                subdivision=form.cleaned_data['subdivision2'],
                subdivision_code=form.cleaned_data['subdivision_code2'],
                dc=form.cleaned_data['dc2'],
                dc_code=form.cleaned_data['dc_code2'],
                reportingDesignation=form.cleaned_data['reportingDesignation2'],
                reportingOfficerCode=form.cleaned_data['reportingOfficerCode2'],
                reportingOfficer=form.cleaned_data['reportingOfficer2'],
                reviewingDesignation=form.cleaned_data['reviewingDesignation2'],
                reviewingOfficerCode=form.cleaned_data['reviewingOfficerCode2'],
                reviewingOfficer=form.cleaned_data['reviewingOfficer2'],
                acceptingDesignation=form.cleaned_data['acceptingDesignation2'],
                acceptingOfficerCode=form.cleaned_data['acceptingOfficerCode2'],
                acceptingOfficer=form.cleaned_data['acceptingOfficer2'],
                hrManager=form.cleaned_data['hrManager2'],
                hrManagerCode=form.cleaned_data['hrManagerCode2'],
                financialYear=form.cleaned_data['financialYear2'],
                isAnotherTagging=form.cleaned_data['isAnotherTagging'],
                isFinal=False
            )
            isAnotherTagging.save()
        response = super().form_valid(form)
        messages.success(self.request, "Employee Tagging has been submitted successfully")
        return response
    def get_context_data(self, *args, **kwargs):
        context = super(TaggingCreateView, self).get_context_data()
        context["session"] = ACR_Session.objects.get(isActive=True)
        return context

@method_decorator(check_valid_referer, name='dispatch')
@method_decorator(login_required(login_url='/login/'), name='dispatch')
class TaggingListView(ListView):
    model = EmployeeTagging
    group_required = [u'Admin', u'Hr',]
    form_class = EmployeeTaggingForm
    context_object_name = 'tagging_view'

    def post(self, request, *args, **kwargs):
        data = EmployeeTagging.objects.get(pk=int(request.POST.get('userid')))
        data.isFinal = True
        data.save()
        return redirect('/mis/')
    def get_context_data(self, **kwargs):
        context = super(TaggingListView, self).get_context_data(**kwargs)
        list = EmployeeTagging.objects.filter(hrManagerCode=self.request.user)
        context["object_list"] = list
        return context

@method_decorator(check_valid_referer, name='dispatch')
@method_decorator(login_required(login_url='/login/'), name='dispatch')
class TaggingUpdateView(UpdateView):
    model = EmployeeTagging
    group_required = [u'Admin', u'Hr', ]
    form_class = EmployeeTaggingUpdateForm
    template_name = 'Accounts/employeetagging_form_update.html'
    success_url = "/mis/"

    def get_context_data(self, *args, **kwargs):
        context = super(TaggingUpdateView, self).get_context_data()
        session = ACR_Session.objects.get(isActive=True)
        context["session"] = session
        return context

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@ratelimit(key='post:empCode',rate='10/m',block=True)
def Login(request):
    if request.user.is_authenticated and request.session['totp_verified']:return redirect('Dashboard')
    if request.method == 'POST':
        if request.POST.get('empCode') == str(request.session.get('empCode')) and request.POST.get('password') == request.session.get('password'):
            user = CustomUser.objects.get(empCode=request.POST.get('empCode'))
            hotp = pyotp.HOTP(user.otpSecretKey)
            if hotp.verify(request.POST.get('otp'), user.otpCounter):
                request.session['totp_verified'] = True
                request.session['totp_attempts'] = 0
                user = authenticate(request, empCode=request.POST.get('empCode'), password=request.POST.get('password'))
                login(request, user)
                return redirect(reverse_lazy('Dashboard'))
            else:
                attempts = request.session.get('totp_attempts', 0)
                attempts += 1
                request.session['totp_attempts'] = attempts
                if attempts >= 5:
                    request.session.flush()
                    return redirect('/')
                else:
                    messages.error(request, ('Invalid OTP code, please try again'))
                    return HttpResponseRedirect('/login/')
        else:
            messages.error(request, ('Invalid Credentials, please try again'))
            return HttpResponseRedirect('/login/')
    else:return render(request, 'login.html')

@check_valid_referer
def logout_view(request):
    logout(request)
    return redirect('/')

@check_valid_referer
def load_posting_data(request):
    if request.GET.get('functionKPI'): return HttpResponse(json.dumps(
        list(kpi.objects.filter(fun_name=request.GET.get('functionKPI')).values_list('kpi_name', flat=True))),
                                                           content_type='application/json')
    if request.GET.get('region'): url = f"{apiUrl}/location/getAllRegions/"
    if request.GET.get('circle'): url = f"{apiUrl}/location/getAllCirclesByRegionId/{request.GET.get('circle')}"
    if request.GET.get('division'): url = f"{apiUrl}/location/getAllDivisionsByCircleId/{request.GET.get('division')}"
    if request.GET.get('subDivision'): url = f"{apiUrl}/location/getAllSubDivisionsByDivisionId/{request.GET.get('subDivision')}"
    if request.GET.get('dc'): url = f"{apiUrl}/location/getAllDcsBySubDivisionId/{request.GET.get('dc')}"
    if request.GET.get('reportingDesignation'): url = f"{apiUrl}/employee/getRoDesignation"
    if request.GET.get('reportingDesignationAll'): url = f"{apiUrl}/employee/getAllDesignation"
    if request.GET.get('designation'): url = f"{apiUrl}/master/getDesignationById?id={request.GET.get('designation')}"
    if request.GET.get('reportingOfficer'): url = f"{apiUrl}/employee/getRoByDesignationId/{request.GET.get('reportingOfficer')}"
    if request.GET.get('function'): url = f"{apiUrl}/master/getAllFunctions/"
    if request.GET.get('functionDesignation'): url = f"{apiUrl}/employee/getRoDesignation"
    response = requests.request("GET", url, verify=False)
    data = response.json()
    if data['code'] == '200' and data['error'] is None:
        if request.GET.get('region'): data['dropdown_type'] = "Region"
        if request.GET.get('circle'): data['dropdown_type'] = "Circle"
        if request.GET.get('division'): data['dropdown_type'] = "Division"
        if request.GET.get('subDivision'): data['dropdown_type'] = "SubDivision"
        if request.GET.get('dc'): data['dropdown_type'] = "DC"
        if request.GET.get('reportingDesignation'): data['dropdown_type'] = "Designation"
        if request.GET.get('reportingDesignationAll'): data['dropdown_type'] = "Designation"
        if request.GET.get('reportingOfficer'): data['dropdown_type'] = "Officer"
        if request.GET.get('function'): data['dropdown_type'] = "Function/Wings"
        if request.GET.get('functionKPI'): data['dropdown_type'] = "KPI"
        if request.GET.get('circle') and HrManagers.objects.filter(regionCode=int(request.GET.get('circle'))).filter(circleCode__isnull=True).exists():data['hrName'] = HrManagers.objects.filter(regionCode=(request.GET.get('circle'))).filter(circleCode__isnull=True).values()[0]
        if request.GET.get('division') and HrManagers.objects.filter(circleCode=int(request.GET.get('division'))).exists():data['hrName'] = HrManagers.objects.filter(circleCode=int(request.GET.get('division'))).values()[0]
        if request.GET.get('functionDesignation'): data['dropdown_type'] = "Designation."
        # print(data)
        return render(request, 'Accounts/dropdown_list_options.html', {'dropdown_data': data})
    else:
        return render(request, 'Accounts/dropdown_list_options.html', {'dropdown_data': response.json()})

@csrf_exempt
@check_valid_referer
@ratelimit(key='post:empCode', rate='5/m', block=True)
def generate_totp(request):
    if request.method == 'POST' and request.POST['type'] == 'login':
        url = f"{apiUrl}/user-login/authenticate"
        urlDetail = f"{apiUrl}/employee/getEmployeeByEmpCode/{request.POST.get('empCode')}"
        payload = json.dumps({
            "username": request.POST.get('empCode'),
            "password": request.POST.get('password'),
            "deviceId": "",
            "requestMode": ""
        })
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        response2 = requests.request("Get", urlDetail, headers=headers, verify=False)
        try:
            if response.json()['code'] == '200' and response.json()['message'] == 'Success' and response2.json()['code'] == '200' and response2.json()['message'] == 'Success':
                secrets = pyotp.random_base32()
                data = response2.json()['list'][0]
                if int(data['designation']['designationClass']) <= 3:
                    if HrManagers.objects.filter(empCode=request.POST.get('empCode')).exists():group = Group.objects.get(name='Hr')
                    else:group = Group.objects.get(name='Employee')
                    if CustomUser.objects.filter(empCode=data['empCode']).exists():
                        user = CustomUser.objects.filter(empCode=data['empCode'])
                        user.update(firstName=data['firstName'], middleName=data['middleName'], lastName=data['lastName'], fullName=data['fullName'], mobileNo=data['mobileNo'], aadhaarNumber=data['adhaarNumber'], dateOfBirth=data['dateOfBirth'], dateOfJoining=data['dateOfJoining'], dateOfTraining=data['dateOfTraining'], gender=data['gender'], fatherName=data['fatherName'], motherName=data['motherName'], maritalStatus=data['maritalStatus'], heightOfEmployee=data['heightOfEmployee'], personalIdentificationMark=data['personalIdentificationMark'], physicallyHandicaped=data['physicallyHandicaped'], percentageOfDisablement=data['percentageOfDisablement'], employmentType=data['employementType'], category=data['category'], email=data['email'], address=data['address'], city=data['city'], region=data['region'], circle=data['circle'], division=data['division'], subDivision=data['subDivision'], dc=data['dc'], substation=data['substation'], defaultShift=data['defaultShift'], designation=data['designation'], reportingOfficer=data['reportingOfficer'], reportingOfficerDesignation=data['reportingOfficerDesignation'], bankName=data['bankName'], bankAccount=data['bankAccount'], bankIfsc=data['bankIfsc'], isReportingOfficer=data['isReportingOfficer'], isManagerHr=data['isManagerHr'], isAeIt=data['isAeIt'], isTransferOrderApprover=data['isTransferOrderApprover'], isCurrentCharge=data['isCurrentCharge'], currentChargeDesignation=data['currentChargeDesignation'], dateOfCurrentCharge=data['dateOfCurrentCharge'], dateOfRegularisation=data['dateOfRegularisation'], managerHr=data['managerHr'], panNo=data['panNo'], managerHrName=data['managerHrName'], attendanceLocationId=data['attendanceLocationId'], departmentId=data['departmentId'], stateOfBirth=data['stateOfBirth'], townOrCityOfBirth=data['townOrCityOfBirth'], isRegisteredHandicapped=data['isRegisteredHandicapped'], discriptionOfHandicapped=data['discriptionOfHandicapped'], officialEmail=data['officialEmail'], gsliNumber=data['gsliNumber'], bloodGroup=data['bloodGroup'], correspondenceAddress=data['correspondenceAddress'], basicPay=data['basicPay'], providentFundType=data['providentFundType'], pranNumber=data['pranNumber'], pfNumber=data['pfNumber'], holidayList=data['holidayList'], deviceId=data['deviceId'], otpSecretKey=secrets, otpCounter=1, status=data['status'])
                        user = CustomUser.objects.get(empCode=data['empCode'])
                        user.set_password(request.POST.get('password'))
                        user.save()
                    else:
                        user = CustomUser(empId=data['id'], empCode=data['empCode'], firstName=data['firstName'], middleName=data['middleName'], lastName=data['lastName'], fullName=data['fullName'], mobileNo=data['mobileNo'], aadhaarNumber=data['adhaarNumber'], dateOfBirth=data['dateOfBirth'], dateOfJoining=data['dateOfJoining'], dateOfTraining=data['dateOfTraining'], gender=data['gender'], fatherName=data['fatherName'], motherName=data['motherName'], maritalStatus=data['maritalStatus'], heightOfEmployee=data['heightOfEmployee'], personalIdentificationMark=data['personalIdentificationMark'], physicallyHandicaped=data['physicallyHandicaped'], percentageOfDisablement=data['percentageOfDisablement'], employmentType=data['employementType'], category=data['category'], email=data['email'], address=data['address'], city=data['city'], region=data['region'], circle=data['circle'], division=data['division'], subDivision=data['subDivision'], dc=data['dc'], substation=data['substation'], defaultShift=data['defaultShift'], designation=data['designation'], reportingOfficer=data['reportingOfficer'], reportingOfficerDesignation=data['reportingOfficerDesignation'], bankName=data['bankName'], bankAccount=data['bankAccount'], bankIfsc=data['bankIfsc'], isReportingOfficer=data['isReportingOfficer'], isManagerHr=data['isManagerHr'], isAeIt=data['isAeIt'], isTransferOrderApprover=data['isTransferOrderApprover'], isCurrentCharge=data['isCurrentCharge'], currentChargeDesignation=data['currentChargeDesignation'], dateOfCurrentCharge=data['dateOfCurrentCharge'], dateOfRegularisation=data['dateOfRegularisation'], managerHr=data['managerHr'], panNo=data['panNo'], managerHrName=data['managerHrName'], attendanceLocationId=data['attendanceLocationId'], departmentId=data['departmentId'], stateOfBirth=data['stateOfBirth'], townOrCityOfBirth=data['townOrCityOfBirth'], isRegisteredHandicapped=data['isRegisteredHandicapped'], discriptionOfHandicapped=data['discriptionOfHandicapped'], officialEmail=data['officialEmail'], gsliNumber=data['gsliNumber'], bloodGroup=data['bloodGroup'], correspondenceAddress=data['correspondenceAddress'], basicPay=data['basicPay'], providentFundType=data['providentFundType'], pranNumber=data['pranNumber'], pfNumber=data['pfNumber'], holidayList=data['holidayList'], deviceId=data['deviceId'], otpSecretKey=secrets, otpCounter=1, status=data['status'],)
                        user.save()
                        group.user_set.add(str(user.pk))
                        user.set_password(request.POST.get('password'))
                        user.save()
                    hotp = pyotp.HOTP(secrets)
                    code = hotp.at(1)
                    request.session['empCode'] = data['empCode']
                    request.session['password'] = request.POST.get('password')
                    response = loginOtp(data["mobileNo"], code)
                    response['code'] = code
                    return JsonResponse(response, safe=False)
                else:return JsonResponse({'status': False, 'message': "You are not authorized to login ACR Portal"}, safe=False)
            else:return JsonResponse({'status': False, 'message': "Invalid Login Credentials"}, safe=False)
        except Exception as e:return JsonResponse({'status': False, 'message': "Invalid Login Credentials"}, safe=False)
    elif request.method == 'POST' and request.POST['type'] == 'forgetPassword':
        url = f"{apiUrl}/employee/getEmployeeByEmpCode/{request.POST.get('empCode')}"
        headers = {'Content-Type': 'application/json'}
        response = requests.request("Get", url, headers=headers, verify=False)
        try:
            if response.json()['code'] == '200' and response.json()['message'] == 'Success' and CustomUser.objects.filter(empCode=request.POST.get('empCode')).exists():
                secrets = pyotp.random_base32()
                data = response.json()['list'][0]
                if CustomUser.objects.filter(empCode=data['empCode']).exists():
                    user = CustomUser.objects.filter(empCode=data['empCode'])
                    user.update(firstName=data['firstName'], middleName=data['middleName'], lastName=data['lastName'],
                                fullName=data['fullName'], mobileNo=data['mobileNo'],
                                aadhaarNumber=data['adhaarNumber'], dateOfBirth=data['dateOfBirth'],
                                dateOfJoining=data['dateOfJoining'], dateOfTraining=data['dateOfTraining'],
                                gender=data['gender'], fatherName=data['fatherName'], motherName=data['motherName'],
                                maritalStatus=data['maritalStatus'], heightOfEmployee=data['heightOfEmployee'],
                                personalIdentificationMark=data['personalIdentificationMark'],
                                physicallyHandicaped=data['physicallyHandicaped'],
                                percentageOfDisablement=data['percentageOfDisablement'],
                                employmentType=data['employementType'], category=data['category'], email=data['email'],
                                address=data['address'], city=data['city'], region=data['region'],
                                circle=data['circle'], division=data['division'], subDivision=data['subDivision'],
                                dc=data['dc'], substation=data['substation'], defaultShift=data['defaultShift'],
                                designation=data['designation'], reportingOfficer=data['reportingOfficer'],
                                reportingOfficerDesignation=data['reportingOfficerDesignation'],
                                bankName=data['bankName'], bankAccount=data['bankAccount'], bankIfsc=data['bankIfsc'],
                                isReportingOfficer=data['isReportingOfficer'], isManagerHr=data['isManagerHr'],
                                isAeIt=data['isAeIt'], isTransferOrderApprover=data['isTransferOrderApprover'],
                                isCurrentCharge=data['isCurrentCharge'],
                                currentChargeDesignation=data['currentChargeDesignation'],
                                dateOfCurrentCharge=data['dateOfCurrentCharge'],
                                dateOfRegularisation=data['dateOfRegularisation'], managerHr=data['managerHr'],
                                panNo=data['panNo'], managerHrName=data['managerHrName'],
                                attendanceLocationId=data['attendanceLocationId'], departmentId=data['departmentId'],
                                stateOfBirth=data['stateOfBirth'], townOrCityOfBirth=data['townOrCityOfBirth'],
                                isRegisteredHandicapped=data['isRegisteredHandicapped'],
                                discriptionOfHandicapped=data['discriptionOfHandicapped'],
                                officialEmail=data['officialEmail'], gsliNumber=data['gsliNumber'],
                                bloodGroup=data['bloodGroup'], correspondenceAddress=data['correspondenceAddress'],
                                basicPay=data['basicPay'], providentFundType=data['providentFundType'],
                                pranNumber=data['pranNumber'], pfNumber=data['pfNumber'],
                                holidayList=data['holidayList'], deviceId=data['deviceId'], otpSecretKey=secrets,
                                otpCounter=1, status=data['status'])
                hotp = pyotp.HOTP(secrets)
                code = hotp.at(1)
                request.session['empCode'] = data['empCode']
                response = loginOtp(data["mobileNo"], code)
                response['code'] = code
                return JsonResponse(response, safe=False)
            else:return JsonResponse({'status': False, 'message': "Invalid Login Credentials"}, safe=False)
        except Exception as e:return JsonResponse({'status': False, 'message': "Invalid Login Credentials"}, safe=False)
    else:return redirect('login')

def forgetPassword(request):
    if request.method == 'POST':
        if request.POST.get('empCode') == str(request.session.get('empCode')):
            user = CustomUser.objects.get(empCode=request.POST.get('empCode'))
            hotp = pyotp.HOTP(user.otpSecretKey)
            if hotp.verify(request.POST.get('otp'), user.otpCounter):
                request.session['totp_attempts'] = 0
                url = f"https://attendance.mpcz.in:8888/E-Attendance/api/user-login/updatePassword"
                payload = json.dumps({
                    "username": request.POST.get('empCode'),
                    "password": request.POST.get('password')
                })
                headers = {'Content-Type': 'application/json'}
                response = requests.request("POST", url, headers=headers, data=payload, verify=False)
                try:messages.success(request, ('Password Changed Successfully!')) if response.json()['code'] == '200' and response.json()['message'] == 'Success' else messages.error(request, (response.text))
                except Exception as e:messages.error(request, (str(e)))
                return redirect(reverse_lazy('login'))
            else:
                attempts = request.session.get('totp_attempts', 0)
                attempts += 1
                request.session['totp_attempts'] = attempts
                if attempts >= 5:
                    request.session.flush()
                    return redirect('/')
                else:
                    messages.error(request, ('Invalid OTP code, please try again'))
                    return HttpResponseRedirect('/forget/password/')
        else:
            messages.error(request, ('Invalid Credentials, please try again'))
            return HttpResponseRedirect('/forget/password/')
    return render(request, 'forgetpassword.html')


'''
Task Before Production
Off code in console and views on login

'''

def generate_pdf(request, taggingId):
    model = EmployeeSelfAppraisal.objects.get(taggingId=taggingId)
    try:
        model.isStatus = True
        html_file = render_to_string('Accounts/employeeappraiseepdf_form.html', {'data': model})
        pdf_content = pdfkit.from_string(html_file, False)
        model.appraisalPdf.save('appraisePdf.pdf', ContentFile(pdf_content))
        response = {'status': 'success', 'message': 'Your ACR has been submitted successfully!'}
    except Exception as e:
        model.isStatus = False
        response = {'status': 'error', 'message': 'Something went wrong, Please try again.'}
    return HttpResponse(response)

def addData(data, typee):
    for i in data:
        if isinstance(i, dict) or isinstance(i, list):
            if typee == "reviewing": i['grade2'] = i['grade']
            elif typee == "reporting":i['grade'] = "N/A"
    return data


def reporting_je_form_hindi(request):
    if request.method == "GET":
        tagging_id=request.GET.get("tagging_id")
        print("+++++++++",tagging_id)
        return render(request,'Accounts/acr_hindi/reporting_je_form_hindi.html',{'tagging_id':tagging_id})

    else:
        i=ReportingOfficer()
        tagging_id=request.POST.get("tagging_id")
        print(tagging_id,"tagging id ye hai ")
        # tagging_data=EmployeeTagging.objects.get(id=tagging_id)
        ReportingOfficer_data=EmployeeTagging.objects.get(id=tagging_id)
        i.reportingofficer_name=ReportingOfficer_data.reportingOfficer
        i.reportingofficer_code=ReportingOfficer_data.reportingOfficerCode
        i.descriptions= request.POST.get("remark")
        print("+++++++++//////////==========",tagging_id)
        i.tagging_id=tagging_id
        # grade= request.POST.get("grade")
        i.grade_one=request.POST.get('Grade1')
        i.grade_two=request.POST.get('Grade2')
        i.grade_three=request.POST.get('Grade3')
        i.grade_four=request.POST.get('Grade4')
        i.grade_five=request.POST.get('Grade5')
        i.grade_six=request.POST.get('Grade6')
        i.grade_seven=request.POST.get('Grade7')
        i.grade_eight=request.POST.get('Grade8')
        i.grade_nine=request.POST.get('Grade9')
        i.grade_ten=request.POST.get('Grade10')
        f_grade=(int(request.POST.get('Grade1'))+
                 int(request.POST.get('Grade2'))+
                 int(request.POST.get('Grade3'))+
                 int(request.POST.get('Grade4'))+
                 int(request.POST.get('Grade5'))+
                 int(request.POST.get('Grade6'))+
                 int(request.POST.get('Grade7'))+
                 int(request.POST.get('Grade8'))+
                 int(request.POST.get('Grade9'))+
                 int(request.POST.get('Grade10')))/10
        i.final_grade=f_grade
        i.is_Status=False
        i.save()
        officer_id=i.id
        print(officer_id,"+=========++=="
            )
        from django.urls import reverse
        url = reverse('reporting_preview',args=[officer_id,tagging_id])
        return redirect(url) 
       
@login_required(login_url='/login/')
def ReportingListView(request):
    data=EmployeeTagging.objects.filter(reportingOfficer__icontains=request.user.empCode).filter(isFinal=True)
    print(data,"=================================")
    return render(request, "Accounts/acr_hindi/emp_tagging_complete_list.html",{'data':data})

def reporting_ta_form_hindi(request):
    if request.method == "GET":
        tagging_id=request.GET.get("tagging_id")
        print("+++++++++",tagging_id)
        return render(request,'Accounts/acr_hindi/reporting_ta_form_hindi.html',{'tagging_id':tagging_id})
    else:
        i=ReportingOfficer()
        tagging_id=request.POST.get("tagging_id")
        ReportingOfficer_data=EmployeeTagging.objects.get(id=tagging_id)
        tagging_data=EmployeeTagging.objects.get(id=tagging_id)
        i.reportingofficer_name=ReportingOfficer_data.reportingOfficer
        i.reportingofficer_code=ReportingOfficer_data.reportingOfficerCode
        i.descriptions= request.POST.get("remark")
        print("+++++++++//////////==========",tagging_id)
        i.tagging__id=tagging_id
        # grade= request.POST.get("grade")
        i.grade_one=request.POST.get('Grade1')
        i.grade_two=request.POST.get('Grade2')
        i.grade_three=request.POST.get('Grade3')
        i.grade_four=request.POST.get('Grade4')
        i.grade_five=request.POST.get('Grade5')
        i.grade_six=request.POST.get('Grade6')
        i.grade_seven=request.POST.get('Grade7')
        f_grade=(int(request.POST.get('Grade1'))+
                 int(request.POST.get('Grade2'))+
                 int(request.POST.get('Grade3'))+
                 int(request.POST.get('Grade4'))+
                 int(request.POST.get('Grade5'))+
                 int(request.POST.get('Grade6'))+
                 int(request.POST.get('Grade7'))
                 )/7
        i.final_grade=f_grade
        i.is_Status=False
        i.save()
        # print(i.f_grade,'+++++++++++++========+++++++++')
        emptype= tagging_data.empCode.employmentType['name']
        emp_des=tagging_data.empCode.designation['name']
        # print(datas,"===============+===============")
        return redirect(reporting_preview)
        return render(request,'Accounts/acr_hindi/preview_officer.html',{'tagging_data':tagging_data,'emptype':emptype,'emp_des':emp_des})
        # print(remark,Grade1,Grade2)
    return render(request,'Accounts/acr_hindi/reporting_ta_form.html',{'tagging_id':tagging_id})


def update_reporting_je_form_hindi(request):
    if request.method == "GET":
        repoting_officer_id=request.GET.get("id")
        print("+++++++++",repoting_officer_id)
        data=ReportingOfficer.objects.get(id=repoting_officer_id)


        return render(request,'Accounts/acr_hindi/update_reporting_je_form.html',{'data':data})
    else:
        reporting_id=request.POST.get("reporting_id")
        i=ReportingOfficer.objects.get(id=reporting_id)
        tagging_id=i.tagging.id        
        ReportingOfficer_data=EmployeeTagging.objects.get(id=i.tagging.id)
        i.reportingofficer_name=ReportingOfficer_data.reportingOfficer
        i.reportingofficer_code=ReportingOfficer_data.reportingOfficerCode

        i.descriptions= request.POST.get("remark")
        # grade= request.POST.get("grade")
        i.grade_one=request.POST.get('Grade1')
        i.grade_two=request.POST.get('Grade2')
        i.grade_three=request.POST.get('Grade3')
        i.grade_four=request.POST.get('Grade4')
        i.grade_five=request.POST.get('Grade5')
        i.grade_six=request.POST.get('Grade6')
        i.grade_seven=request.POST.get('Grade7')
        i.grade_eight=request.POST.get('Grade8')
        i.grade_nine=request.POST.get('Grade9')
        i.grade_ten=request.POST.get('Grade10')
        f_grade=(int (i.grade_one)+
                 int(i.grade_two)+
                 int(i.grade_three)+
                 int(i.grade_four)+
                 int(i.grade_five)+
                 int(i.grade_six)+
                 int(i.grade_seven)+
                 int(i.grade_eight)+
                 int(i.grade_nine)+
                 int(i.grade_ten))/10
        i.final_grade=f_grade
        i.is_Status=False
        i.save()
        officer_id=i.id
        print(officer_id,"+=========++=="
            )
        from django.urls import reverse
        url = reverse('reporting_preview',args=[officer_id,tagging_id])
        return redirect(url)
        return render(request,'Accounts/acr_hindi/preview_officer.html')

    return render(request,'Accounts/acr_hindi/update_reporting_je_form.html')
    pass

def reporting_preview(request,officer_id,tagging_id):
    i=ReportingOfficer.objects.get(id=officer_id)
    tagging_data=EmployeeTagging.objects.get(id=tagging_id)
    emptype= tagging_data.empCode.employmentType['name']
    emp_des=tagging_data.empCode.designation['name']
    g_one=int(i.grade_one)
    g_two=int(i.grade_two)
    g_three=int(i.grade_three)
    g_four=int(i.grade_four)
    g_five=int(i.grade_five)
    g_six=int(i.grade_six)
    g_seven=int(i.grade_seven)
    g_eight =int(i.grade_eight)
    g_nine=int(i.grade_nine)
    g_ten=int(i.grade_ten)
    description=i.descriptions,
    

    return render(request,'Accounts/acr_hindi/preview_officer.html',{'tagging_data':tagging_data,'emptype':emptype,'emp_des':emp_des,'reported_data':i,'g_one':g_one,
            'g_two':g_two,
            'g_three':g_three,
            'g_four':g_four,
            'g_five':g_five,
            'g_six':g_six,
            'g_seven':g_seven,
            'g_eight':g_eight,
            'g_nine':g_nine,
            'g_ten':g_ten,
            'description':description,
            'i':i
            })

def generate_pdf_reporting_officer(request):
    if request.method == "GET":
        repoting_officer_id=request.GET.get("id")
        tagging_id=request.GET.get('tagging_id')
        model = ReportingOfficer.objects.get(id=repoting_officer_id)
        i=ReportingOfficer.objects.get(id=repoting_officer_id)
        tagging_data=EmployeeTagging.objects.get(id=tagging_id)
        emptype= tagging_data.empCode.employmentType['name']
        emp_des=tagging_data.empCode.designation['name']
        g_one=int(i.grade_one)
        g_two=int(i.grade_two)
        g_three=int(i.grade_three)
        g_four=int(i.grade_four)
        g_five=int(i.grade_five)
        g_six=int(i.grade_six)
        g_seven=int(i.grade_seven)
        g_eight =int(i.grade_eight)
        g_nine=int(i.grade_nine)
        g_ten=int(i.grade_ten)
        description=i.descriptions,
    
        
        model.is_Status = True

        html_file = render_to_string('Accounts/acr_hindi/preview_officer.html',{'tagging_data':tagging_data,'emptype':emptype,'emp_des':emp_des,'reported_data':i,'g_one':g_one,'g_two':g_two,'g_three':g_three,'g_four':g_four,'g_five':g_five,'g_six':g_six,'g_seven':g_seven,'g_eight':g_eight,'g_nine':g_nine,'g_ten':g_ten,'description':description,'i':i
            })
        # config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf")
        config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
        # 
        pdf_content = pdfkit.from_string(html_file, False,configuration = config)
        model.reporting_pdf.save('ReportingOfficerPdf.pdf', ContentFile(pdf_content))
       
        return HttpResponse("somthing went wrong")
    

def generate_pdf(request, taggingId):
    model = EmployeeSelfAppraisal.objects.get(taggingId=taggingId)
    try:
        model.isStatus = True
        html_file = render_to_string('Accounts/employeeappraiseepdf_form.html', {'data': model})
        pdf_content = pdfkit.from_string(html_file, False)
        model.appraisalPdf.save('appraisePdf.pdf', ContentFile(pdf_content))
        response = {'status': 'success', 'message': 'Your ACR has been submitted successfully!'}
    except Exception as e:
        model.isStatus = False
        response = {'status': 'error', 'message': 'Something went wrong, Please try again.'}
    return HttpResponse(response)
