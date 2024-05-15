from django.test import TestCase

# def registerEmployee(request):
#     workbook = openpyxl.load_workbook('Accounts/EMPCODE.xlsx')
#     sheet = workbook.active
#     for row in sheet.iter_rows():
#         for cell in row:
#             empCode = str(cell.value)
#             try:
#                 urlDetail = f"{apiUrl}/employee/getEmployeeByEmpCode/{empCode}"
#                 headers = {'Content-Type': 'application/json'}
#                 response2 = requests.request("Get", urlDetail, headers=headers, verify=False)
#                 if response2.json()['code'] == '200' and response2.json()['message'] == 'Success':
#                     secrets = pyotp.random_base32()
#                     data = response2.json()['list'][0]
#                     if HrManagers.objects.filter(empCode=empCode).exists():group = Group.objects.get(name='Hr')
#                     else:group = Group.objects.get(name='Employee')
#                     if CustomUser.objects.filter(empCode=data['empCode']).exists():
#                         user = CustomUser.objects.filter(empCode=data['empCode'])
#                         user.update(firstName=data['firstName'], middleName=data['middleName'], lastName=data['lastName'], fullName=data['fullName'], mobileNo=data['mobileNo'], aadhaarNumber=data['adhaarNumber'], dateOfBirth=data['dateOfBirth'], dateOfJoining=data['dateOfJoining'], dateOfTraining=data['dateOfTraining'], gender=data['gender'], fatherName=data['fatherName'], motherName=data['motherName'], maritalStatus=data['maritalStatus'], heightOfEmployee=data['heightOfEmployee'], personalIdentificationMark=data['personalIdentificationMark'], physicallyHandicaped=data['physicallyHandicaped'], percentageOfDisablement=data['percentageOfDisablement'], employmentType=data['employementType'], category=data['category'], email=data['email'], address=data['address'], city=data['city'], region=data['region'], circle=data['circle'], division=data['division'], subDivision=data['subDivision'], dc=data['dc'], substation=data['substation'], defaultShift=data['defaultShift'], designation=data['designation'], reportingOfficer=data['reportingOfficer'], reportingOfficerDesignation=data['reportingOfficerDesignation'], bankName=data['bankName'], bankAccount=data['bankAccount'], bankIfsc=data['bankIfsc'], isReportingOfficer=data['isReportingOfficer'], isManagerHr=data['isManagerHr'], isAeIt=data['isAeIt'], isTransferOrderApprover=data['isTransferOrderApprover'], isCurrentCharge=data['isCurrentCharge'], currentChargeDesignation=data['currentChargeDesignation'], dateOfCurrentCharge=data['dateOfCurrentCharge'], dateOfRegularisation=data['dateOfRegularisation'], managerHr=data['managerHr'], panNo=data['panNo'], managerHrName=data['managerHrName'], attendanceLocationId=data['attendanceLocationId'], departmentId=data['departmentId'], stateOfBirth=data['stateOfBirth'], townOrCityOfBirth=data['townOrCityOfBirth'], isRegisteredHandicapped=data['isRegisteredHandicapped'], discriptionOfHandicapped=data['discriptionOfHandicapped'], officialEmail=data['officialEmail'], gsliNumber=data['gsliNumber'], bloodGroup=data['bloodGroup'], correspondenceAddress=data['correspondenceAddress'], basicPay=data['basicPay'], providentFundType=data['providentFundType'], pranNumber=data['pranNumber'], pfNumber=data['pfNumber'], holidayList=data['holidayList'], deviceId=data['deviceId'], otpSecretKey=secrets, otpCounter=1, status=data['status'])
#                         user = CustomUser.objects.get(empCode=data['empCode'])
#                         user.set_password("Pass@123")
#                         user.save()
#
#                     else:
#                         user = CustomUser( empId=data['id'], empCode=data['empCode'], firstName=data['firstName'], middleName=data['middleName'], lastName=data['lastName'], fullName=data['fullName'], mobileNo=data['mobileNo'], aadhaarNumber=data['adhaarNumber'], dateOfBirth=data['dateOfBirth'], dateOfJoining=data['dateOfJoining'], dateOfTraining=data['dateOfTraining'], gender=data['gender'], fatherName=data['fatherName'], motherName=data['motherName'], maritalStatus=data['maritalStatus'], heightOfEmployee=data['heightOfEmployee'], personalIdentificationMark=data['personalIdentificationMark'], physicallyHandicaped=data['physicallyHandicaped'], percentageOfDisablement=data['percentageOfDisablement'], employmentType=data['employementType'], category=data['category'], email=data['email'], address=data['address'], city=data['city'], region=data['region'], circle=data['circle'], division=data['division'], subDivision=data['subDivision'], dc=data['dc'], substation=data['substation'], defaultShift=data['defaultShift'], designation=data['designation'], reportingOfficer=data['reportingOfficer'], reportingOfficerDesignation=data['reportingOfficerDesignation'], bankName=data['bankName'], bankAccount=data['bankAccount'], bankIfsc=data['bankIfsc'], isReportingOfficer=data['isReportingOfficer'], isManagerHr=data['isManagerHr'], isAeIt=data['isAeIt'], isTransferOrderApprover=data['isTransferOrderApprover'], isCurrentCharge=data['isCurrentCharge'], currentChargeDesignation=data['currentChargeDesignation'], dateOfCurrentCharge=data['dateOfCurrentCharge'], dateOfRegularisation=data['dateOfRegularisation'], managerHr=data['managerHr'], panNo=data['panNo'], managerHrName=data['managerHrName'], attendanceLocationId=data['attendanceLocationId'], departmentId=data['departmentId'], stateOfBirth=data['stateOfBirth'], townOrCityOfBirth=data['townOrCityOfBirth'], isRegisteredHandicapped=data['isRegisteredHandicapped'], discriptionOfHandicapped=data['discriptionOfHandicapped'], officialEmail=data['officialEmail'], gsliNumber=data['gsliNumber'], bloodGroup=data['bloodGroup'], correspondenceAddress=data['correspondenceAddress'], basicPay=data['basicPay'], providentFundType=data['providentFundType'], pranNumber=data['pranNumber'], pfNumber=data['pfNumber'], holidayList=data['holidayList'], deviceId=data['deviceId'], otpSecretKey=secrets, otpCounter=1, status=data['status'],)
#                         user.save()
#                         group.user_set.add(str(user.pk))
#                         user.set_password("Pass@123")
#                         user.save()
#                     with open('Success.txt', 'a') as f:
#                         f.write(str(empCode) + '\n')
#                     f.close()
#                 else:
#                     with open('Errorresp.txt', 'a') as f:
#                         f.write(str(empCode) + '\n')
#                     f.close()
#             except Exception as e:
#                 with open('Exceptions.txt', 'a') as f:
#                     f.write(str(e) + str(empCode) + '\n')
#                 f.close()
#                 with open('ExceptionsCode.txt', 'a') as f:
#                     f.write(str(empCode) + '\n')
#                 f.close()


# def generate_pdf(request):
#     html_string = render_to_string('Accounts/employeeappraiseepdf_form.html', {'data': EmployeeSelfAppraisal.objects.get(taggingId=16)})
#     pdf_file = HttpResponse(content_type='application/pdf')
#     pdf_file['Content-Disposition'] = 'attachment; filename="output.pdf"'
#     pisa.CreatePDF(html_string, dest=pdf_file, encoding='UTF-8')
#     pdf_file.close()
#     # html_file = render_to_string('Accounts/employeeappraiseepdf_form.html', {'data': EmployeeSelfAppraisal.objects.get(taggingId=16)})
#     # output_pdf = 'output.pdf'
#     # pdfkit.from_string(html_file, output_pdf)
#     # print("PDF created successfully!")
#     # return HttpResponse("PDF created successfully!")
#     # return HttpResponse(html_string)
#     return pdf_file

# def data_normalize(request):
#     lst = ["24"]
#     for i in lst:
#         user = EmployeeTagging.objects.get(pk=i)
#         if user.dc and not user.dc_code:
#             url = f"{apiUrl}/location/getAllDcsBySubDivisionId/{user.subdivision_code}"
#             response = requests.request("GET", url, verify=False)
#             data = response.json()['list']
#             for val in data:
#                 if user.dc in str(val):
#                     user.dc_code = val['dcId']
#                     user.save()
#     return HttpResponse("No Error Found")
# Create your tests here.


