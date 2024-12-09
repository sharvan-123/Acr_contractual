from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
#from django_ratelimit.decorators import ratelimit
from dateutil.relativedelta import relativedelta
from django.core.files.base import ContentFile
from django.shortcuts import render
from ACRPortal.settings import config
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
    print(request.user.employmentType['empTypeId'],request.user.designation['designationId'],"type id............")
    if request.user.employmentType['empTypeId']== 6 and (request.user.designation['designationId']==  98 or 99) :
        is_tagging=True
    else:
        is_tagging=False
    print(is_tagging)
    user = request.user
    user_groups = user.groups.all()
    group_names = [group.name for group in user_groups]

    context = {
        'group_names': group_names,
        'is_tagging':is_tagging
    }
    return render(request, 'index.html',context)


@method_decorator(check_valid_referer, name='dispatch')
@method_decorator(login_required(login_url='/login/'), name='dispatch')
@method_decorator(check_valid_dates('Tagging'), name='dispatch')
class TaggingCreateView(CreateView):
    model = EmployeeTagging
    form_class = EmployeeTaggingForm
    context_object_name = 'tagging_add'
    success_url = reverse_lazy('tagging_add')
    def form_valid(self, form):
        print("form ke aNDR HAI")
        print(form.cleaned_data['fromDate'])
        print(form.cleaned_data['toDate'])
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

    # def get_context_data(self, *args, **kwargs):
    #     context = super(TaggingUpdateView, self).get_context_data()
    #     # session = ACR_Session.objects.get(isActive=True)
    #     # context["session"] = session
    #     # return context

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
#@ratelimit(key='post:empCode',rate='10/m',block=True)
def Login(request):
    if request.user.is_authenticated and request.session['totp_verified']:return redirect('Dashboard')
    if request.method == 'POST':
        if request.POST.get('empCode') == str(request.session.get('empCode')) and request.POST.get('password') == request.session.get('password'):
            user = CustomUser.objects.get(empCode=request.POST.get('empCode'))
            hotp = pyotp.HOTP(user.otpSecretKey)
            response = verifyOtp(user.mobileNo,request.POST.get('otp'))
            print("reponse++++++",response['code'])
            if response['code']=="200":
            # if hotp.verify(request.POST.get('otp'), user.otpCounter):
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
#@ratelimit(key='post:empCode', rate='5/m', block=True)
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
                return JsonResponse(response, safe=False)
            else:return JsonResponse({'status': False, 'message': "Invalid Login Credentials"}, safe=False)
        except Exception as e:return JsonResponse({'status': False, 'message': "Invalid Login Credentials"}, safe=False)
    else:return redirect('login')

def forgetPassword(request):
    if request.method == 'POST':
        if request.POST.get('empCode') == str(request.session.get('empCode')):
            user = CustomUser.objects.get(empCode=request.POST.get('empCode'))
            hotp = pyotp.HOTP(user.otpSecretKey)
            # if hotp.verify(request.POST.get('otp'), user.otpCounter):
            response = verifyOtp(user.mobileNo,request.POST.get('otp'))
            print("reponse++++++",response['code'])
            if response['code']=="200":
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

@login_required(login_url='/login/')
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
    print(request.user.mobileNo,"mobile no.....",data)
    flag=[]
    JE_TA_data=[]
    for i in data:
        if i.empCode.designation['designationId'] == 99 or i.empCode.designation['designationId']== 98:
            JE_TA_data.append(0)
        elif i.empCode.designation['designationId'] == 84 or i.empCode.designation['designationId']== 37:
            JE_TA_data.append(1)
        reporting_officer = ReportingOfficer.objects.filter(tagging__id=i.id).filter(is_Status=True)

        print('reporting officer',reporting_officer)
        if reporting_officer:
            flag.append(0)
        else:
            flag.append(1)
    data1=zip(data,flag,JE_TA_data)
    return render(request, "Accounts/acr_hindi/emp_tagging_complete_list.html",{'final_data':data1})

@login_required(login_url='/login/')
def reporting_ta_form_hindi(request):
    if request.method == "GET":
        tagging_id=request.GET.get("tagging_id")
        print("+++++++++",tagging_id)
        return render(request,'Accounts/acr_hindi/reporting_ta_form.html',{'tagging_id':tagging_id})
    else:
        i=ReportingOfficer()
        tagging_id=request.POST.get("tagging_id")
        ReportingOfficer_data=EmployeeTagging.objects.get(id=tagging_id)
        tagging_data=EmployeeTagging.objects.get(id=tagging_id)
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
        officer_id=i.id
        # print(i.f_grade,'+++++++++++++========+++++++++')
        emptype= tagging_data.empCode.employmentType['name']
        emp_des=tagging_data.empCode.designation['name']
        # print(datas,"===============+===============")
        from django.urls import reverse
        url = reverse('reporting_ta_preview',args=[officer_id,tagging_id])
        return redirect(url)
        return render(request,'Accounts/acr_hindi/preview_officer.html',{'tagging_data':tagging_data,'emptype':emptype,'emp_des':emp_des})
        # print(remark,Grade1,Grade2)
    return render(request,'Accounts/acr_hindi/reporting_ta_form.html',{'tagging_id':tagging_id})

@login_required(login_url='/login/')
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


@login_required(login_url='/login/')
def update_reporting_ta_form_hindi(request):
    if request.method == "GET":
        repoting_officer_id=request.GET.get("id")
        print("+++++++++repoting_officer_id",repoting_officer_id)
        data=ReportingOfficer.objects.get(id=repoting_officer_id)


        return render(request,'Accounts/acr_hindi/update_reporting_ta_form.html',{'data':data})
    else:
        reporting_id=request.POST.get("reporting_id")
        print(reporting_id,"12345678987654321234567")
        i=ReportingOfficer.objects.filter(id=reporting_id).first()
        tagging_id=i.tagging_id

        print(i,tagging_id,"sumit parmar")        
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
        f_grade=(int (i.grade_one)+
                 int(i.grade_two)+
                 int(i.grade_three)+
                 int(i.grade_four)+
                 int(i.grade_five)+
                 int(i.grade_six))/7
        i.final_grade=f_grade
        i.is_Status=False
        i.save()
        officer_id=i.id
        print(officer_id,"+=========++=="
            )
        from django.urls import reverse
        url = reverse('reporting_ta_preview',args=[officer_id,tagging_id])
        return redirect(url)


@login_required(login_url='/login/')
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


@login_required(login_url='/login/')
def reporting_ta_preview(request,officer_id,tagging_id):
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
    description=i.descriptions,
    

    return render(request,'Accounts/acr_hindi/preview_ta_officer.html',{'tagging_data':tagging_data,'emptype':emptype,'emp_des':emp_des,'reported_data':i,'g_one':g_one,
            'g_two':g_two,
            'g_three':g_three,
            'g_four':g_four,
            'g_five':g_five,
            'g_six':g_six,
            'g_seven':g_seven,
            'description':description,
            'i':i
            })



# def generate_pdf_reporting_officer(request):
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
import pdfkit
from datetime import datetime

def generate_pdf_reporting_officer(request):
    print("its call a this function")
    secrets = pyotp.random_base32()
    hotp = pyotp.HOTP(secrets)
    code = hotp.at(1)
    flag=request.POST.get("flag")
    print(code,flag,"bheja hua flag")
    if flag is None:
        response = loginOtp(request.user.mobileNo, code)
        # LoginOtp.objects.create(emp_id=request.user.id,otp=code)
        # response['code'] = code
        user = request.user
        # hotp = pyotp.HOTP(user.otpSecretKey)
    repoting_officer_id = request.GET.get("id")
    tagging_id = request.GET.get('tagging_id')
    print(repoting_officer_id,tagging_id,"repoting_officer_idrepoting_officer_idrepoting_officer_idrepoting_officer_id")
    if request.method == "POST":
        user = CustomUser.objects.get(empCode=request.user.empCode)
        hotp = pyotp.HOTP(user.otpSecretKey)
        print("?????????????")
        repoting_officer_id = request.POST.get("repoting_officer_id")
        tagging_id = request.POST.get('tagging_id')
        print(request.POST.get('otp'),repoting_officer_id,tagging_id,"post wali method", user.otpCounter,request.user.otpSecretKey)
        # if code == request.POST.get('otp'):
        # if hotp.verify(request.POST.get('otp'), user.otpCounter):
        # if LoginOtp.objects.filter(emp_id=request.user.id,otp=request.POST.get('otp')).exists():
        response = verifyOtp(request.user.mobileNo,request.POST.get('otp'))
        # print("reponse++++++",response['code'])
        if response['code']=="200":
            request.session['totp_verified'] = True
            request.session['totp_attempts'] = 0
            repoting_officer_id = request.POST.get("repoting_officer_id")
            tagging_id = request.POST.get('tagging_id')
            print("repoting_officer_id",repoting_officer_id,"tagging_id",tagging_id,"post method call ")
            model = ReportingOfficer.objects.get(id=repoting_officer_id)
            current_time = datetime.now()
            if model.grade_eight is not None:
                tagging_data = EmployeeTagging.objects.get(id=tagging_id)
                emptype = tagging_data.empCode.employmentType['name']
                emp_des = tagging_data.empCode.designation['name']
                g_one = int(model.grade_one)
                g_two = int(model.grade_two)
                g_three = int(model.grade_three)
                g_four = int(model.grade_four)
                g_five = int(model.grade_five)
                g_six = int(model.grade_six)
                g_seven = int(model.grade_seven)
                g_eight = int(model.grade_eight)
                g_nine = int(model.grade_nine)
                g_ten = int(model.grade_ten)
                description = model.descriptions
                html_file = render_to_string(
                    # 'Accounts/acr_hindi/test.html',
                    'Accounts/acr_hindi/pdf_genrate_reportingofficer.html',
                    {
                        'tagging_data': tagging_data,
                        'emptype': emptype,
                        'emp_des': emp_des,
                        'reported_data': model,
                        'g_one': g_one,
                        'g_two': g_two,
                        'g_three': g_three,
                        'g_four': g_four,
                        'g_five': g_five,
                        'g_six': g_six,
                        'g_seven': g_seven,
                        'g_eight': g_eight,
                        'g_nine': g_nine,
                        'g_ten': g_ten,
                        'description': description,
                        'i': model,
                        'current_time':current_time,
                    }
                )
                conf = pdfkit.configuration(wkhtmltopdf=config)
                pdf_content = pdfkit.from_string(html_file,False,configuration=conf)

                model.reporting_pdf.save(str(tagging_data.empCode)+'_ReportingPdf.pdf', ContentFile(pdf_content))
                model.is_Status = True
                model.save()
                # LoginOtp.objects.filter(emp_id=request.user.id,otp=request.POST.get('otp')).delete()
                return redirect(ReportingListView)
            else:
                tagging_data = EmployeeTagging.objects.get(id=tagging_id)
                emptype = tagging_data.empCode.employmentType['name']
                emp_des = tagging_data.empCode.designation['name']
                g_one = int(model.grade_one)
                g_two = int(model.grade_two)
                g_three = int(model.grade_three)
                g_four = int(model.grade_four)
                g_five = int(model.grade_five)
                g_six = int(model.grade_six)
                g_seven = int(model.grade_seven)
                description = model.descriptions
                html_file = render_to_string(
                    # 'Accounts/acr_hindi/test.html'
                    'Accounts/acr_hindi/pdf_genrate_ta_reportingofficer.html',
                    {
                        'tagging_data': tagging_data,
                        'emptype': emptype,
                        'emp_des': emp_des,
                        'reported_data': model,
                        'g_one': g_one,
                        'g_two': g_two,
                        'g_three': g_three,
                        'g_four': g_four,
                        'g_five': g_five,
                        'g_six': g_six,
                        'g_seven': g_seven,
                        'description': description,
                        'i': model,
                        'current_time':current_time
                    }
                )
                conf = pdfkit.configuration(wkhtmltopdf=config)
                pdf_content = pdfkit.from_string(html_file,False,configuration=conf)
                model.reporting_pdf.save(str(tagging_data.empCode)+'_ReportingPdf.pdf', ContentFile(pdf_content))
                model.is_Status = True
                model.save()
                # LoginOtp.objects.filter(emp_id=request.user.id,otp=request.POST.get('otp')).delete()
                return redirect(ReportingListView)
                
        else:
            attempts = request.session.get('totp_attempts', 0)
            attempts += 1
            request.session['totp_attempts'] = attempts
            if attempts >= 5:
                request.session.flush()
                return redirect('/')
            else:
                messages.error(request, ('Invalid OTP code, please try again'))
                from django.urls import reverse
                officer_id=repoting_officer_id
                url = reverse('reporting_preview',args=[officer_id,tagging_id])
                return redirect(url)
    return render(request,"Accounts/acr_hindi/otp_reportingofficer.html",{'repoting_officer_id':repoting_officer_id,'tagging_id':tagging_id})


@login_required(login_url='/login/')
def reportingOtp(request):
    secrets = pyotp.random_base32()
    hotp = pyotp.HOTP(secrets)
    code = hotp.at(1)
    response = loginOtp(request.user.mobileNo, code)
    response['code'] = code
    user = CustomUser.objects.get(empCode=request.POST.get('empCode'))
    hotp = pyotp.HOTP(user.otpSecretKey)
    if hotp.verify(request.POST.get('otp'), user.otpCounter):
        request.session['totp_attempts'] = 0
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

    return redirect(generate_pdf_reporting_officer)



@login_required(login_url='/login/')
def ReviewingListView(request):
    data2=EmployeeTagging.objects.filter(reviewingOfficer__icontains=request.user.empCode).filter(isFinal=True)
    flag=[]
    data1=[]
    for i in data2:
        data = ReportingOfficer.objects.filter(tagging__id=i.id,is_Status=True)
        reviewing_officer=""
        if data:
            for j in data:
                reviewing_officer=ReviewingOfficer.objects.filter(tagging__id=j.tagging.id,is_Status=True)
                if reviewing_officer:
                    flag.append(0)
                else:
                    flag.append(1)
        print(flag)
        data1=zip(data,flag)
        
    return render(request, "Accounts/acr_hindi/reporting_complete_list.html",{'final_data':data1})

@login_required(login_url='/login/')
def reviewingOfficer_form(request,tagging_id):
    reporting_officer_data = ReportingOfficer.objects.get(tagging_id=tagging_id,is_Status=True)
    tagging_data=EmployeeTagging.objects.get(id=tagging_id)
    emptype= tagging_data.empCode.employmentType['name']
    emp_des=tagging_data.empCode.designation['name']
    reportingGrade=float(reporting_officer_data.final_grade)
    if request.method == "POST":
        print(tagging_id)
        i=ReviewingOfficer()
        # i.tagging__id=tagging_id
        print(request.POST.get('tagging_id'),"++++++++++++++++++++++++++")
        i.final_grade=request.POST.get('final_grade')
        i.descriptions=request.POST.get('remark')
        i.tagging_id=request.POST.get('tagging_id')
        i.is_Status=False
        i.save()
        from django.urls import reverse
        url = reverse('reviewing_preview',args=[tagging_id])
        return redirect(url)
    return render(request,'Accounts/acr_hindi/reviewing_form.html',{'tagging_id':tagging_id,'tagging_data':tagging_data,'emptype':emptype,'emp_des':emp_des,'reportingGrade':reportingGrade,'reporting_officer_data':reporting_officer_data})



@login_required(login_url='/login/')
def reviewing_preview(request,tagging_id):
    reporting_data=ReportingOfficer.objects.get(tagging__id=tagging_id)
    tagging_data=EmployeeTagging.objects.get(id=tagging_id)
    reviewing_data=ReviewingOfficer.objects.get(tagging__id=tagging_id)
    emptype= tagging_data.empCode.employmentType['name']
    emp_des=tagging_data.empCode.designation['name']
    reporting_grade=float(reporting_data.final_grade) 
    reviewing_grade=float(reviewing_data.final_grade)
    return render(request,'Accounts/acr_hindi/preview_reviewing.html',{'tagging_data':tagging_data,'emptype':emptype,'emp_des':emp_des,
            'g_ten':reporting_grade,
            'reviewing_data':reviewing_data,
            'reviewing_grade':reviewing_grade,
            'reporting_data':reporting_data,
            'reviewing_data':reviewing_data
            })


@login_required(login_url='/login/')
def update_reviewing_form_hindi(request,tagging_id):
    if request.method == "GET":
        reporting_data=ReviewingOfficer.objects.get(tagging_id=tagging_id)
        reviewingdata=ReviewingOfficer.objects.get(tagging_id=tagging_id)
        tagging_data=EmployeeTagging.objects.get(id=tagging_id)
        reporting_data=ReportingOfficer.objects.get(tagging__id=tagging_id)
        reviewing_data=ReviewingOfficer.objects.get(tagging__id=tagging_id)
        emptype= tagging_data.empCode.employmentType['name']
        emp_des=tagging_data.empCode.designation['name']
        reporting_grade=float(reporting_data.final_grade) 
        reviewing_grade=reviewing_data.final_grade
        return render(request,'Accounts/acr_hindi/update_reviewing_form.html',{'emptype':emptype,
                                                                               'emp_des':emp_des,
                                                                               'tagging_data':tagging_data,
                                                                               'reporting_grade':reporting_grade,
                                                                               'reviewing_grade':reviewing_grade,
                                                                               'reporting_data':reporting_data,
                                                                               'reviewing_data':reviewing_data
                                                                              })
    else:
        print(tagging_id,"qwertyuiopoiuytrewertyuioiuytrewertyuiuytre")
        i=ReviewingOfficer.objects.get(tagging__id=tagging_id)
        tagging_id=i.tagging.id    
        i.final_grade=request.POST.get('final_grade')
        i.descriptions=request.POST.get('remark')
        i.is_Status=False
        i.save()
        officer_id=i.id
        from django.urls import reverse
        url = reverse('reviewing_preview',args=[tagging_id])
        return redirect(url)


# def generate_pdf_reporting_officer(request):
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
import pdfkit
@login_required(login_url='/login/')
def generate_pdf_reviewing_officer(request):
    print("its call a this function")
    secrets = pyotp.random_base32()
    hotp = pyotp.HOTP(secrets)
    code = hotp.at(1)
    flag=request.POST.get("flag")
    print(code,flag,"bheja hua flag")
    if flag is None:
        response = loginOtp(request.user.mobileNo, code)
        # LoginOtp.objects.create(emp_id=request.user.id,otp=code)
        # response['code'] = code
        user = request.user
        # hotp = pyotp.HOTP(user.otpSecretKey)
    tagging_id = request.GET.get('tagging_id')
    # print(repoting_officer_id,tagging_id,"repoting_officer_idrepoting_officer_idrepoting_officer_idrepoting_officer_id")
    if request.method == "POST":
        user = CustomUser.objects.get(empCode=request.user.empCode)
        hotp = pyotp.HOTP(user.otpSecretKey)
        print("?????????????")
        tagging_id = request.POST.get('tagging_id')
        # print(request.POST.get('otp'),tagging_id,"post wali method", user.otpCounter,request.user.otpSecretKey)
        # if code == request.POST.get('otp'):
        # if hotp.verify(request.POST.get('otp'), user.otpCounter):
        # if LoginOtp.objects.filter(emp_id=request.user.id,otp=request.POST.get('otp')).exists():
        response = verifyOtp(request.user.mobileNo,request.POST.get('otp'))
        # print("reponse++++++",response['code'])
        if response['code']=="200":
            request.session['totp_verified'] = True
            request.session['totp_attempts'] = 0
            # repoting_officer_id = request.POST.get("repoting_officer_id")
            tagging_id = request.POST.get('tagging_id')
            # print("repoting_officer_id",repoting_officer_id,"tagging_id",tagging_id,"post method call ")
            reporting_model = ReportingOfficer.objects.get(tagging__id=tagging_id)
            reviewing_model=ReviewingOfficer.objects.get(tagging__id=tagging_id)
            tagging_data = EmployeeTagging.objects.get(id=tagging_id)
            emptype = tagging_data.empCode.employmentType['name']
            emp_des = tagging_data.empCode.designation['name']
            reviewing_grade=float(reviewing_model.final_grade)
            reporting_grade=float(reporting_model.final_grade)
            current_time = datetime.now()
            html_file = render_to_string(
                # 'Accounts/acr_hindi/test.html',
                'Accounts/acr_hindi/pdf_genrate_reviewingofficer.html',
                {
                    'tagging_data': tagging_data,
                    'emptype': emptype,
                    'emp_des': emp_des,
                    'reviewing_grade':reviewing_grade,
                    'reporting_grade':reporting_grade,
                    'tagging_data':tagging_data,
                    'reporting_model':reporting_model,
                    'reviewing_model':reviewing_model,
                    'current_time':current_time
                }
            )
            conf = pdfkit.configuration(wkhtmltopdf=config)
            pdf_content = pdfkit.from_string(html_file,False,configuration=conf)
            reviewing_model.reviewing_officer_pdf.save(str(tagging_data.empCode)+'_ReviewingOfficerPdf.pdf', ContentFile(pdf_content))
            reviewing_model.is_Status = True
            reviewing_model.save()
            # LoginOtp.objects.filter(emp_id=request.user.id,otp=request.POST.get('otp')).delete()
            return redirect(ReviewingListView)
        else:
            attempts = request.session.get('totp_attempts', 0)
            attempts += 1
            request.session['totp_attempts'] = attempts
            if attempts >= 5:
                request.session.flush()
                return redirect('/')
            else:
                messages.error(request, ('Invalid OTP code, please try again'))
                from django.urls import reverse
                
                url = reverse('reviewing_preview',args=[tagging_id])
                return redirect(url)
    return render(request,"Accounts/acr_hindi/otp_reviewingofficer.html",{'tagging_id':tagging_id})


@login_required(login_url='/login/')
def AcceptingListView(request):
    data=EmployeeTagging.objects.filter(acceptingOfficer__icontains=request.user.empCode).filter(isFinal=True)
    print(request.user.mobileNo,"mobile no.....")
    flag=[]
    data1=zip([0],[0])
    for i in data:
        print(i.id,"tagging id ..........")
        reviewing_officer = ReviewingOfficer.objects.filter(tagging__id=i.id,is_Status=True)
        accepting_officer = AcceptingOfficer.objects.filter(tagging__id=i.id,is_Status=True)

        for j in reviewing_officer:
            if accepting_officer:
                flag.append(1)
            else:
                flag.append(0)
        data1=zip(reviewing_officer,flag)
    
        print(reviewing_officer,accepting_officer,"+++++++++++++++++++++",flag)
        # for j,k in data1:
        #     print(j,k)
    return render(request, "Accounts/acr_hindi/reviewing_complete_list.html",{'final_data':data1})

@login_required(login_url='/login/')
def acceptingOfficer_form(request,tagging_id):
    # tagging_id=request.GET.get('tagging_id')
    # print("tagging_id...............",tagging_id)
    # tagging_data=EmployeeTagging.objects.filter(id=tagging_id)
    # print(tagging_id,'123456523456y543456434567')
    tagging_data=EmployeeTagging.objects.get(id=tagging_id)
    emptype= tagging_data.empCode.employmentType['name']
    emp_des=tagging_data.empCode.designation['name']
    reporting_officer_data = ReportingOfficer.objects.get(tagging__id=tagging_id,is_Status=True)
    reviewing_officer_data=ReviewingOfficer.objects.get(tagging__id=tagging_id,is_Status=True)
    reportingGrade=float(reporting_officer_data.final_grade)
    reviewingGrade=float(reviewing_officer_data.final_grade)
    if request.method == "POST":
        print(tagging_id)
        i=AcceptingOfficer()
        # i.tagging__id=tagging_id
        print(request.POST.get('tagging_id'),"++++++++++++++++++++++++++")
        i.final_grade=request.POST.get('final_grade')
        i.tagging_id=request.POST.get('tagging_id')
        i.descriptions=request.POST.get('remark')
        i.is_Status=False
        i.save()
        from django.urls import reverse
        url = reverse('accepting_preview',args=[tagging_id])
        return redirect(url)
        return HttpResponse("data saved")
    return render(request,'Accounts/acr_hindi/accepting_form.html',{'tagging_id':tagging_id,'tagging_data':tagging_data,'emptype':emptype,'emp_des':emp_des,'reportingGrade':reportingGrade,'reviewingGrade':reviewingGrade,'reporting_officer_data':reporting_officer_data,'reviewing_officer_data':reviewing_officer_data})

@login_required(login_url='/login/')
def accepting_preview(request,tagging_id):
    # i=ReportingOfficer.objects.get(id=officer_id)
    tagging_data=EmployeeTagging.objects.get(id=tagging_id)
    reporting_data=ReportingOfficer.objects.get(tagging__id=tagging_id)
    reviewing_data=ReviewingOfficer.objects.get(tagging__id=tagging_id)
    accepting_data1=AcceptingOfficer.objects.get(tagging__id=tagging_id)
    emptype= tagging_data.empCode.employmentType['name']
    emp_des=tagging_data.empCode.designation['name']
    reporting_grade=float(reporting_data.final_grade) 
    reviewing_grade=float(reviewing_data.final_grade)
    accepting_data=float(accepting_data1.final_grade)


    return render(request,'Accounts/acr_hindi/preview_accepting.html',{'tagging_data':tagging_data,'emptype':emptype,'emp_des':emp_des,
            'g_ten':reporting_grade,
            'accepting_data':accepting_data,
            'reviewing_grade':reviewing_grade,
            'accepting_data1':accepting_data1,
            'reporting_data':reporting_data,
            'reviewing_data':reviewing_data
            })

@login_required(login_url='/login/')
def update_accepting_form_hindi(request,tagging_id):
    if request.method == "GET":
        # tagging_data=EmployeeTagging.objects.get(id=tagging_id)
        # tagging_id=request.GET.get("id")
        print("++++ttttt+++++",tagging_id)
        # reporting_data=ReviewingOfficer.objects.get(tagging_id=tagging_id)
        # reviewingdata=ReviewingOfficer.objects.get(tagging_id=tagging_id)
        tagging_data=EmployeeTagging.objects.get(id=tagging_id)
        reporting_data=ReportingOfficer.objects.get(tagging__id=tagging_id)
        reviewing_data=ReviewingOfficer.objects.get(tagging__id=tagging_id)
        accepting_data=AcceptingOfficer.objects.get(tagging__id=tagging_id)
        emptype= tagging_data.empCode.employmentType['name']
        emp_des=tagging_data.empCode.designation['name']
        reporting_grade=float(reporting_data.final_grade) 
        reviewing_grade=float(reviewing_data.final_grade)
        accepting_grade=accepting_data.final_grade
        print('accepting_grade',accepting_grade)


        return render(request,'Accounts/acr_hindi/update_accepting_form.html',{'emptype':emptype,
                                                                               'emp_des':emp_des,
                                                                               'tagging_data':tagging_data,
                                                                               'reporting_grade':reporting_grade,
                                                                               'reviewing_grade':reviewing_grade,
                                                                               'accepting_grade':accepting_grade,
                                                                               'accepting_data':accepting_data,
                                                                               'reviewing_data':reviewing_data,
                                                                               'reporting_data':reporting_data
                                                                              })
    else:
        # tagging_id=request.POST.get("tagging_id")
        # print(tagging_id,"qwertyuiopoiuytrewertyuioiuytrewertyuiuytre")
        i=AcceptingOfficer.objects.get(tagging__id=tagging_id)
        tagging_id=i.tagging.id    
        # tagging_data=EmployeeTagging.objects.get(id=i.tagging.id)
        i.final_grade=request.POST.get('final_grade')
        i.descriptions=request.POST.get('remark')
        i.is_Status=False
        i.save()
        officer_id=i.id
        print(officer_id,"+=========++=="
            )
        from django.urls import reverse
        url = reverse('accepting_preview',args=[tagging_id])
        return redirect(url)


@login_required(login_url='/login/')
def generate_pdf_accepting_officer(request):
    print("its call a this function")
    secrets = pyotp.random_base32()
    hotp = pyotp.HOTP(secrets)
    code = hotp.at(1)
    flag=request.POST.get("flag")
    print(code,flag,"bheja hua flag")
    if flag is None:
        response = loginOtp(request.user.mobileNo, code)
        # LoginOtp.objects.create(emp_id=request.user.id,otp=code)
        # response['code'] = code
        user = request.user
        # hotp = pyotp.HOTP(user.otpSecretKey)
    tagging_id = request.GET.get('tagging_id')
    # print(repoting_officer_id,tagging_id,"repoting_officer_idrepoting_officer_idrepoting_officer_idrepoting_officer_id")
    if request.method == "POST":
        user = CustomUser.objects.get(empCode=request.user.empCode)
        hotp = pyotp.HOTP(user.otpSecretKey)
        tagging_id = request.POST.get('tagging_id')
        # print(request.POST.get('otp'),tagging_id,"post wali method", user.otpCounter,request.user.otpSecretKey)
        # if code == request.POST.get('otp'):
        # if hotp.verify(request.POST.get('otp'), user.otpCounter):
        # if LoginOtp.objects.filter(emp_id=request.user.id,otp=request.POST.get('otp')).exists():
        response = verifyOtp(request.user.mobileNo,request.POST.get('otp'))
        # print("reponse++++++",response['code'])
        if response['code']=="200":
            request.session['totp_verified'] = True
            request.session['totp_attempts'] = 0
            # repoting_officer_id = request.POST.get("repoting_officer_id")
            tagging_id = request.POST.get('tagging_id')
            # print("repoting_officer_id",repoting_officer_id,"tagging_id",tagging_id,"post method call ")
            reporting_model = ReportingOfficer.objects.get(tagging__id=tagging_id)
            reviewing_model=ReviewingOfficer.objects.get(tagging__id=tagging_id)
            accepting_model=AcceptingOfficer.objects.get(tagging__id=tagging_id)
            tagging_data = EmployeeTagging.objects.get(id=tagging_id)
            emptype = tagging_data.empCode.employmentType['name']
            emp_des = tagging_data.empCode.designation['name']
            reviewing_grade=float(reviewing_model.final_grade)
            reporting_grade=float(reporting_model.final_grade)
            accepting_grade=float(accepting_model.final_grade)
            current_time = datetime.now()
            html_file = render_to_string(
                # 'Accounts/acr_hindi/test.html',
                'Accounts/acr_hindi/pdf_genrate_acceptingofficer.html',
                {
                    'tagging_data': tagging_data,
                    'emptype': emptype,
                    'emp_des': emp_des,
                    'reviewing_grade':reviewing_grade,
                    'reporting_grade':reporting_grade,
                    'accepting_grade':accepting_grade,
                    'tagging_data':tagging_data,
                    'reporting_model':reporting_model,
                    'reviewing_model':reviewing_model,
                    'accepting_model':accepting_model,
                    'current_time':current_time
                }
            )
            # path_to_wkhtmltopdf = r'usr/local/bin/wkhtmltopdf.exe' # Update this path
            conf = pdfkit.configuration(wkhtmltopdf=config)
            pdf_content = pdfkit.from_string(html_file,False,configuration=conf)
            accepting_model.accepting_officer_pdf.save(str(tagging_data.empCode)+'_AcceptingOfficerPdf.pdf', ContentFile(pdf_content))
            accepting_model.is_Status = True
            accepting_model.save()
            # LoginOtp.objects.filter(emp_id=request.user.id,otp=request.POST.get('otp')).delete()
            return redirect(AcceptingListView)
        else:
            attempts = request.session.get('totp_attempts', 0)
            attempts += 1
            request.session['totp_attempts'] = attempts
            if attempts >= 5:
                request.session.flush()
                return redirect('/')
            else:
                messages.error(request, ('Invalid OTP code, please try again'))
                from django.urls import reverse
                
                url = reverse('accepting_preview',args=[tagging_id])
                return redirect(url)
            
    print("data saved")
    return render(request,"Accounts/acr_hindi/otp_accepting_officer.html",{'tagging_id':tagging_id})



from django.db.models import Q
def emp_tagging_form_ta(request):
    if request.method=="GET":
        emp_detail=CustomUser.objects.filter(employmentType__empTypeId=6 ,designation__designationId__in=[37,84])
        # region_url = f"{apiUrl}/location/getAllRegions/"
        # import requests
        # response = requests.get(region_url)
        # if response.status_code == 200:
        #     data = response.json()
        #     print(data)
        #     # result = CustomUser.objects.filter(
        #     # Q(designation__n='Asst. Engineer') &
        #     # Q(employmentType__empTypeId=6))
        context={
                'emp_detail':emp_detail
            }
    else:
        tagging=EmployeeTagging()
        print("is_final check",request.POST.get('is_final'))
        isanotherTagging1=request.POST.get("isanotherTagging1")
        tagging_id=CustomUser.objects.get(empCode=request.POST.get("empCode"))
        tagging.empCode_id=tagging_id.id
        tagging.fromDate=request.POST.get("from_Date")
        tagging.toDate=request.POST.get("toDate")
        tagging.region=request.POST.get("region")
        tagging.region_code=request.POST.get("region_code")
        # tagging.region_code=2233
        tagging.circle=request.POST.get("circle")
        # tagging.circle_code=1122
        tagging.circle_code=request.POST.get("circle_code")
        tagging.division=request.POST.get("division")
        tagging.division_code=request.POST.get("division_code")
        # tagging.division_code=444555
        tagging.subdivision=request.POST.get("subdivision")
        # tagging.subdivision_code=111222333
        tagging.subdivision_code=request.POST.get("subdivision_code")
        tagging.dc=request.POST.get("dc")
        # tagging.dc_code=11223344
        tagging.dc_code=request.POST.get("dc_code")
        tagging.reportingDesignation=request.POST.get("reportingDesignation_one")
        tagging.reportingOfficerCode=request.POST.get("reportingOfficerCode")
        tagging.reportingOfficer=request.POST.get("reportingOfficer")
        tagging.reviewingDesignation=request.POST.get("reviewingDesignation_one")
        tagging.reviewingOfficerCode=request.POST.get("reviewingOfficerCode")
        tagging.reviewingOfficer=request.POST.get("reviewingOfficer")
        tagging.acceptingDesignation=request.POST.get("acceptingDesignation_one")
        tagging.acceptingOfficerCode=request.POST.get("acceptingOfficerCode")
        tagging.acceptingOfficer=request.POST.get("acceptingOfficer")
        tagging.financialYear='2023-24'
        if request.POST.get("region_code") is not None and request.POST.get("circle_code") is not None and request. POST.get("circle_code") != "" :
            hr_manager_data=HrManagers.objects.filter(circleCode=request.POST.get("circle_code")).first()
            tagging.hrManager=hr_manager_data.empName
            tagging.hrManagerCode=hr_manager_data.empCode
            
        elif request.POST.get("region_code") is not None and (request.POST.get("circle_code") is None or request.POST.get("circle_code") == ""):
            hr_manager_data=HrManagers.objects.filter(regionCode=request.POST.get("region_code")).first()
        # print(hr_manager_data,"+++++++=======+++++++",hr_manager_data.empName,hr_manager_data.empCode,"hr data 2")
            tagging.hrManager=hr_manager_data.empName
            tagging.hrManagerCode=hr_manager_data.empCode
            
        # tagging.isAnotherTagging=request.POST.get("isAnotherTagging")
        if isanotherTagging1 == '1':
            tagging.isAnotherTagging=True
        else:
            tagging.isAnotherTagging=False
        if request.POST.get('is_final') == 'True' :
            tagging.isFinal=True
        else:
            tagging.isFinal=False
        tagging.save()
        if isanotherTagging1 == '1':
            tagging2=EmployeeTagging()

            tagging_id=CustomUser.objects.get(empCode=request.POST.get("empCode"))
            tagging2.empCode_id=tagging_id.id
            tagging2.fromDate=request.POST.get("from_Date2")
            tagging2.toDate=request.POST.get("toDate2")
            tagging2.region=request.POST.get("region2")
            tagging2.region_code=request.POST.get("region_code2")
            # taggi2ng.region_code=2233
            tagging2.circle=request.POST.get("circle2")
            # taggi2ng.circle_code=1122
            tagging2.circle_code=request.POST.get("circle_code2")
            tagging2.division=request.POST.get("division2")
            tagging2.division_code=request.POST.get("division_code2")
            tagging2.subdivision=request.POST.get("subdivision2")
            # taggi2ng.subdivision_code=111222333
            tagging2.subdivision_code=request.POST.get("subdivision_code2")
            tagging2.dc=request.POST.get("dc2")
            tagging2.dc_code=request.POST.get("dc_code2")
            tagging2.reportingDesignation=request.POST.get("reportingDesignation_two")
            tagging2.reportingOfficerCode=request.POST.get("reportingOfficerCode2")
            tagging2.reportingOfficer=request.POST.get("reportingOfficer2")
            tagging2.reviewingDesignation=request.POST.get("reviewingDesignation_two")
            tagging2.reviewingOfficerCode=request.POST.get("reviewingOfficerCode2")
            tagging2.reviewingOfficer=request.POST.get("reviewingOfficer2")
            tagging2.acceptingDesignation=request.POST.get("acceptingDesignation_two")
            tagging2.acceptingOfficerCode=request.POST.get("acceptingOfficerCode2")
            tagging2.acceptingOfficer=request.POST.get("acceptingOfficer2")
            if request.POST.get("region_code2") is not None and request.POST.get("circle_code2") is not None and request. POST.get("circle_code2") != "" :
                hr_manager_data=HrManagers.objects.filter(circleCode=request.POST.get("circle_code2")).first()
            elif request.POST.get("region_code2") is not None and (request.POST.get("circle_code2") is None or request.POST.get("circle_code2") == ""):
                hr_manager_data=HrManagers.objects.filter(regionCode=request.POST.get("region_code2")).first()
            tagging2.hrManager=hr_manager_data.empName
            tagging2.hrManagerCode=hr_manager_data.empCode
            # taggi2ng.hrManager=request.POST.get("hrManager2")
            # taggi2ng.hrManagerCode=request.POST.get("hrManagerCode2")
            tagging2.financialYear='2023-24'
            if request.POST.get('is_final') == 'True' :
                tagging.isFinal=True
            else:
                tagging.isFinal=False
            tagging2.isAnotherTagging=True
            tagging2.save()

        return redirect(dashboard)
        # print(emp_detail,"all details of ta form ")

    return render(request,"Accounts/employeetagging_form_ta.html",context)



from django.db.models import Q
def emp_tagging_form_je(request):
    if request.method== "POST":
        if EmployeeTagging.objects.filter(empCode_id=request.user.id).exists():
            print("if ke adnar hai...........")
            # messages.error("tagging already submitted")
            messages.error(request, ('Tagging already submitted'))
        else:
            print("esle ke adnar hai...........")
            tagging=EmployeeTagging()
            print("is_final check",request.POST.get('is_final'))
            isanotherTagging1=request.POST.get("isanotherTagging1")
            tagging.empCode_id=request.user.id
            tagging.fromDate=request.POST.get("from_Date")
            tagging.toDate=request.POST.get("toDate")
            tagging.region=request.POST.get("region")
            tagging.region_code=request.POST.get("region_code")
            # tagging.region_code=2233
            tagging.circle=request.POST.get("circle")
            # tagging.circle_code=1122
            tagging.circle_code=request.POST.get("circle_code")
            tagging.division=request.POST.get("division")
            tagging.division_code=request.POST.get("division_code")
            # tagging.division_code=444555
            tagging.subdivision=request.POST.get("subdivision")
            # tagging.subdivision_code=111222333
            tagging.subdivision_code=request.POST.get("subdivision_code")
            tagging.dc=request.POST.get("dc")
            # tagging.dc_code=11223344
            tagging.dc_code=request.POST.get("dc_code")
            tagging.reportingDesignation=request.POST.get("reportingDesignation_one")
            tagging.reportingOfficerCode=request.POST.get("reportingOfficerCode")
            tagging.reportingOfficer=request.POST.get("reportingOfficer")
            tagging.reviewingDesignation=request.POST.get("reviewingDesignation_one")
            tagging.reviewingOfficerCode=request.POST.get("reviewingOfficerCode")
            tagging.reviewingOfficer=request.POST.get("reviewingOfficer")
            tagging.acceptingDesignation=request.POST.get("acceptingDesignation_one")
            tagging.acceptingOfficerCode=request.POST.get("acceptingOfficerCode")
            tagging.acceptingOfficer=request.POST.get("acceptingOfficer")
            tagging.financialYear='2023-24'
            if request.POST.get("region_code") is not None and request.POST.get("circle_code") is not None and request. POST.get("circle_code") != "" :
                hr_manager_data=HrManagers.objects.filter(circleCode=request.POST.get("circle_code")).first()
                tagging.hrManager=hr_manager_data.empName
                tagging.hrManagerCode=hr_manager_data.empCode
                
            elif request.POST.get("region_code") is not None and (request.POST.get("circle_code") is None or request.POST.get("circle_code") == ""):
                hr_manager_data=HrManagers.objects.filter(regionCode=request.POST.get("region_code")).first()
            # print(hr_manager_data,"+++++++=======+++++++",hr_manager_data.empName,hr_manager_data.empCode,"hr data 2")
                tagging.hrManager=hr_manager_data.empName
                tagging.hrManagerCode=hr_manager_data.empCode
                
            # tagging.isAnotherTagging=request.POST.get("isAnotherTagging")
            if isanotherTagging1 == '1':
                tagging.isAnotherTagging=True
            else:
                tagging.isAnotherTagging=False
            if request.POST.get('is_final') == 'True' :
                tagging.isFinal=True
            else:
                tagging.isFinal=False
            tagging.save()
            if isanotherTagging1 == '1':
                tagging2=EmployeeTagging()
                tagging2.empCode_id=request.user.id
                tagging2.fromDate=request.POST.get("from_Date2")
                tagging2.toDate=request.POST.get("toDate2")
                tagging2.region=request.POST.get("region2")
                tagging2.region_code=request.POST.get("region_code2")
                # taggi2ng.region_code=2233
                tagging2.circle=request.POST.get("circle2")
                # taggi2ng.circle_code=1122
                tagging2.circle_code=request.POST.get("circle_code2")
                tagging2.division=request.POST.get("division2")
                tagging2.division_code=request.POST.get("division_code2")
                tagging2.subdivision=request.POST.get("subdivision2")
                # taggi2ng.subdivision_code=111222333
                tagging2.subdivision_code=request.POST.get("subdivision_code2")
                tagging2.dc=request.POST.get("dc2")
                tagging2.dc_code=request.POST.get("dc_code2")
                tagging2.reportingDesignation=request.POST.get("reportingDesignation_two")
                tagging2.reportingOfficerCode=request.POST.get("reportingOfficerCode2")
                tagging2.reportingOfficer=request.POST.get("reportingOfficer2")
                tagging2.reviewingDesignation=request.POST.get("reviewingDesignation_two")
                tagging2.reviewingOfficerCode=request.POST.get("reviewingOfficerCode2")
                tagging2.reviewingOfficer=request.POST.get("reviewingOfficer2")
                tagging2.acceptingDesignation=request.POST.get("acceptingDesignation_two")
                tagging2.acceptingOfficerCode=request.POST.get("acceptingOfficerCode2")
                tagging2.acceptingOfficer=request.POST.get("acceptingOfficer2")
                if request.POST.get("region_code2") is not None and request.POST.get("circle_code2") is not None and request. POST.get("circle_code2") != "" :
                    hr_manager_data=HrManagers.objects.filter(circleCode=request.POST.get("circle_code2")).first()
                elif request.POST.get("region_code2") is not None and (request.POST.get("circle_code2") is None or request.POST.get("circle_code2") == ""):
                    hr_manager_data=HrManagers.objects.filter(regionCode=request.POST.get("region_code2")).first()
                tagging2.hrManager=hr_manager_data.empName
                tagging2.hrManagerCode=hr_manager_data.empCode
                # taggi2ng.hrManager=request.POST.get("hrManager2")
                # taggi2ng.hrManagerCode=request.POST.get("hrManagerCode2")
                tagging2.financialYear='2023-24'
                if request.POST.get('is_final') == 'True' :
                    tagging.isFinal=True
                else:
                    tagging.isFinal=False
                tagging2.isAnotherTagging=True
                tagging2.save()

        return redirect(dashboard)
        # print(emp_detail,"all details of ta form ")

    return render(request,"Accounts/employeetagging_form_je.html")

#150033
# def complete_acr_list(request):
#     print(request.user.empCode,"codddddddddddddd")
#     if request.user.empCode == '12345678':
#         # tagging_data1=EmployeeTagging.objects.filter(empCode__designation['designationId']==99)
#         tagging_data1 = EmployeeTagging.objects.filter(empCode__designation__contains={'designationId': 37},isFinal=True)
#         accepting_data=[]
#         reviewing_data=[]
#         reporting_data=[]
#         for i in tagging_data1:
#             # print(i.id,"id jo loop me hai")
#             accepting_data1=AcceptingOfficer.objects.filter(tagging__id=i.id,is_Status=True)
#             accepting_data.append(accepting_data1)

#             reviewing_data1=ReviewingOfficer.objects.filter(tagging__id=i.id,is_Status=True)
#             reviewing_data.append(reviewing_data1)
            
#             reporting_data1=ReportingOfficer.objects.filter(tagging__id=i.id,is_Status=True)
#             reporting_data.append(reporting_data1)
            
#         print()
#         data=zip(accepting_data,reviewing_data,reporting_data)
#         print(accepting_data,reviewing_data1,tagging_data1,"+++++++++++++++")        
#         return render(request,'Accounts/acr_hindi/complete_acr_list.html',{'data':data
#         })
#     else:
#         print("qwertyuiopoiuytrew12345678")
#         accepting_data=AcceptingOfficer.objects.filter(is_Status=True)
#         reviewing_data=[]
#         reporting_data=[]
#         tagging_data=[]
#         for i in accepting_data:
#         # emp_data=EmployeeTagging.objects.filter(id=accepting_data.tagging.id)
#             reviewing_data1=ReviewingOfficer.objects.get(tagging__id=i.tagging.id)
#             reviewing_data.append(reviewing_data1)
#             reporting_data1=ReportingOfficer.objects.get(tagging__id=i.tagging.id)
#             reporting_data.append(reporting_data1)
#             tagging_data1=EmployeeTagging.objects.get(id=i.tagging.id)
#             tagging_data.append(tagging_data1)
#         data=zip(accepting_data,reviewing_data,reporting_data,tagging_data)
#         print(accepting_data,reviewing_data,tagging_data)        
#     return render(request,'Accounts/acr_hindi/complete_acr_list.html',{'data':data})

def complete_acr_list(request):
    # tagging_data1=EmployeeTagging.objects.filter(empCode__designation['designationId']==99)
    if request.user.empCode == '150033' or '12345678':
        tagging_data1 = list(EmployeeTagging.objects.filter(
        empCode__designation__designationId=98,
        isFinal=True
        ).values_list('id',flat=True))
    elif request.user.region is not None and request.user.circle is None and request.user.groups.filter(name='Hr').exists():
        tagging_data1 = list(EmployeeTagging.objects.filter(
        empCode__designation__designationId__in=[37,99],region_code=request.user.region['regionId'],       
        isFinal=True
        ).values_list('id',flat=True))
    elif request.user.region is not None and request.user.circle is not None and request.user.groups.filter(name='Hr').exists():
        tagging_data1 = list(EmployeeTagging.objects.filter(
        empCode__designation__designationId=84,region_code=request.user.region['regionId'],circle_code=request.user.circle['circleId'],     
        isFinal=True
        ).values_list('id',flat=True))

    accepting_data1=AcceptingOfficer.objects.filter(tagging__id__in=tagging_data1,is_Status=True)
    reviewing_data1=ReviewingOfficer.objects.filter(tagging__id__in=tagging_data1,is_Status=True)
    reporting_data1=ReportingOfficer.objects.filter(tagging__id__in=tagging_data1,is_Status=True)
    off_list=[]
    data=[]
    for i in reporting_data1:
        off_list.append(i)

    for j in off_list:
        data2=[]
        data2.append(j.tagging.empCode.fullName)
        if j.reporting_pdf:
            data2.append(j)
        else:
            data2.append(0)
        reviewing_data2=ReviewingOfficer.objects.filter(tagging__id__in=tagging_data1,is_Status=True,tagging__empCode=j.tagging.empCode).first()
        if reviewing_data2:
            data2.append(reviewing_data2)
        else:
            data2.append(0)
        accepting_data2=AcceptingOfficer.objects.filter(tagging__id__in=tagging_data1,is_Status=True,tagging__empCode=j.tagging.empCode).first()
        if accepting_data2:
            data2.append(accepting_data2)
        else:
            data2.append(0)
        data.append(data2)
    # print(data,"fianl data")
        
    c=0
    for i in accepting_data1:
        c+=1
    # print(c,"QQQQQQQQQQQQQQQQQQQ")
    # print(accepting_data,reviewing_data1,tagging_data1,"+++++++++++++++")        
    return render(request,'Accounts/acr_hindi/complete_acr_list.html',{'final_data':data
    })