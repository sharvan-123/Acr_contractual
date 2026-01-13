import os

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.contrib.postgres.fields import JSONField


state_choices = (("Andhra Pradesh","Andhra Pradesh"),("Arunachal Pradesh ","Arunachal Pradesh "),("Assam","Assam"),("Bihar","Bihar"),("Chhattisgarh","Chhattisgarh"),("Goa","Goa"),("Gujarat","Gujarat"),("Haryana","Haryana"),("Himachal Pradesh","Himachal Pradesh"),("Jammu and Kashmir ","Jammu and Kashmir "),("Jharkhand","Jharkhand"),("Karnataka","Karnataka"),("Kerala","Kerala"),("Madhya Pradesh","Madhya Pradesh"),("Maharashtra","Maharashtra"),("Manipur","Manipur"),("Meghalaya","Meghalaya"),("Mizoram","Mizoram"),("Nagaland","Nagaland"),("Odisha","Odisha"),("Punjab","Punjab"),("Rajasthan","Rajasthan"),("Sikkim","Sikkim"),("Tamil Nadu","Tamil Nadu"),("Telangana","Telangana"),("Tripura","Tripura"),("Uttar Pradesh","Uttar Pradesh"),("Uttarakhand","Uttarakhand"),("West Bengal","West Bengal"),("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),("Chandigarh","Chandigarh"),("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),("Daman and Diu","Daman and Diu"),("Lakshadweep","Lakshadweep"),("National Capital Territory of Delhi","National Capital Territory of Delhi"),("Puducherry","Puducherry"))
gender = (('Male','Male'),('Female','Female'),('Transgender','Transgender'),)
OPTIONS = [('YES', 'YES'),('NO', 'NO'),]
personalJson = [
    {'personal':'Attitude to work','marks':'(1-10)','grade':''},
    {'personal':'Sense of responsibility, maintain sustained quality output. Commitment towards objective (1-10) number.','marks':'(1-10)','grade':''},
    {'personal':'Decision making ability and judgement.','marks':'(1-10)','grade':''},
    {'personal':'Ability to inspire and motivate and take initiatives (1-10) number.','marks':'(1-10)','grade':''},
    {'personal':'Communication skill (Written and oral) (1-10) number.', 'marks': '(1-10)', 'grade': ''},
    {'personal':'Inter-Personal relation and team work.', 'marks': '(1-10)', 'grade': ''},
    {'personal':'Self Appraisal/Reporting remarks submitted on time or not (* MANDATORY If YES - 10/ If NO - 0) 0 if auto - forwarded or 10 by System O.', 'marks': '(1-10)', 'grade': '10'},
]

def get_user_folder(instance, filename):
    return os.path.join(str(instance.taggingId.empCode), filename)
def get_user_folder_reporting_class_3(instance, filename):
    return os.path.join(str(instance.reportingOfficerCode), filename)
def get_user_folder_reviewing_class_3(instance, filename):
    return os.path.join(str(instance.reviewingOfficerCode), filename)
def get_user_folder_accepting_class_3(instance, filename):
    return os.path.join(str(instance.acceptingOfficerCode), filename)

# get_user_folder = lambda instance, filename: os.path.join(str(instance.empCode), filename)
# get_user_folder_reporting_class_3 = lambda instance, filename: os.path.join(str(instance.reportingOfficerCode), filename)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = None
    empId = models.IntegerField(_('Employee Id'), unique=True)
    empCode = models.CharField(_('Employee Code'), max_length=12, unique=True)
    firstName = models.CharField(_('First Name'), max_length=100,default='', null=True,blank=True)
    middleName = models.CharField(_('Middle Name'), max_length=100,default='', null=True,blank=True)
    lastName = models.CharField(_('Last Name'), max_length=100,default='', null=True,blank=True)
    fullName = models.CharField(_('Full Name'), max_length=100,default='', null=True,blank=True)
    mobileNo = models.CharField(_('Mobile Number'), max_length=10, null=True, blank=True)
    aadhaarNumber = models.CharField(_('Aadhaar Card Number'), max_length=12, null=True, blank=True)
    dateOfBirth = models.DateField(_('Date Of Birth'), null=True,blank=True)
    dateOfJoining = models.DateField(_('Date Of Joining'), null=True,blank=True)
    dateOfTraining = models.DateField(_('Date Of Training'), null=True,blank=True)
    gender = models.CharField(_('Gender'), choices=gender, max_length=50, null=True,blank=True)
    fatherName = models.CharField(_('Father Name'), max_length=100,default='', null=True,blank=True)
    motherName = models.CharField(_('Mother Name'), max_length=100,default='', null=True,blank=True)
    maritalStatus = models.CharField(_('Marital Status'), max_length=100,default='', null=True,blank=True)
    heightOfEmployee = models.FloatField(_('Height Of Employee'), null=True, blank=True)
    personalIdentificationMark = models.CharField(_('Personal Identification Mark'), max_length=100,default='', null=True,blank=True)
    physicallyHandicaped = models.CharField(_('Physically Handicapped'), max_length=100,default='', null=True,blank=True)
    percentageOfDisablement = models.CharField(_('Percentage Of Disablement'), max_length=100,default='', null=True,blank=True)
    employmentType = models.JSONField(null=True, blank=True)
    category = models.CharField(_('Category'), max_length=50, null=True,blank=True)
    email = models.EmailField(_('Email Id'), null=True,blank=True)
    address = models.CharField(_('Address'), max_length=250, null=True, blank=True)
    city = models.CharField(_('City'), max_length=250, null=True, blank=True)
    region = models.JSONField(null=True, blank=True)
    circle = models.JSONField( null=True, blank=True)
    division = models.JSONField( null=True, blank=True)
    subDivision = models.JSONField( null=True, blank=True)
    dc = models.JSONField(null=True, blank=True)
    substation = models.JSONField(null=True, blank=True)
    defaultShift = models.JSONField(null=True, blank=True)
    designation = models.JSONField(null=True, blank=True)
    reportingOfficer = models.JSONField(null=True, blank=True)
    reportingOfficerDesignation = models.JSONField( null=True, blank=True)
    bankName = models.CharField(_('Bank Name'), max_length=250, null=True, blank=True)
    bankAccount = models.CharField(_('Bank Account'), max_length=250, null=True, blank=True)
    bankIfsc = models.CharField(_('Bank Ifsc'), max_length=250, null=True, blank=True)
    isReportingOfficer = models.BooleanField(default=False, null=True, blank=True)
    isManagerHr = models.BooleanField(default=False, null=True, blank=True)
    isAeIt = models.BooleanField(default=False, null=True, blank=True)
    isScnIssuer = models.BooleanField(default=False, null=True, blank=True)
    isTransferOrderApprover = models.BooleanField(default=False, null=True, blank=True)
    isCurrentCharge = models.BooleanField(default=False, null=True, blank=True)
    currentChargeDesignation = models.CharField(_('Current Charge Designation'), max_length=250, null=True, blank=True)
    dateOfCurrentCharge = models.CharField(_('Date Of Current Charge'), max_length=250, null=True, blank=True)
    dateOfRegularisation = models.CharField(_('Date Of Regularisation'), max_length=250, null=True, blank=True)
    managerHr = models.JSONField(null=True, blank=True)
    panNo = models.CharField(_('Pan No'), max_length=250, null=True, blank=True)
    managerHrName = models.CharField(_('Manager Hr Name'), max_length=250, null=True, blank=True)
    attendanceLocationId = models.JSONField(null=True, blank=True)
    departmentId = models.CharField(_('Department Id'), max_length=250, null=True, blank=True)
    stateOfBirth = models.CharField(_('State Of Birth'), max_length=250, null=True, blank=True)
    townOrCityOfBirth = models.CharField(_('Town Or City Of Birth'), max_length=250, null=True, blank=True)
    isRegisteredHandicapped = models.BooleanField(default=False, null=True, blank=True)
    discriptionOfHandicapped = models.CharField(_('Discription Of Handicapped'), max_length=250, null=True, blank=True)
    officialEmail = models.CharField(_('Official Email'), max_length=250, null=True, blank=True)
    gsliNumber = models.CharField(_('Gsli Number'), max_length=250, null=True, blank=True)
    bloodGroup = models.CharField(_('Blood Group'), max_length=250, null=True, blank=True)
    correspondenceAddress = models.CharField(_('Correspondence Address'), max_length=250, null=True, blank=True)
    basicPay = models.CharField(_('Basic Pay'), max_length=250, null=True, blank=True)
    providentFundType = models.CharField(_('Provident Fund Type'), max_length=250, null=True, blank=True)
    pranNumber = models.CharField(_('Pran Number'), max_length=250, null=True, blank=True)
    pfNumber = models.CharField(_('Pf Number'), max_length=250, null=True, blank=True)
    holidayList = models.JSONField(null=True, blank=True)
    deviceId = models.CharField(_('Device Id'), max_length=250, null=True, blank=True)
    otpSecretKey = models.CharField(_('hotp_secret_key'), max_length=50, null=True, blank=True)
    otpCounter = models.PositiveIntegerField(_('hotp_counter'), null=True, blank=True)
    status = models.CharField(_('Status'), max_length=50,null=True, blank=True)

    # Permissions
    is_login = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    date_joined = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)


    USERNAME_FIELD = 'empCode'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return str(self.empCode)


class EmployeeTagging(models.Model):

    empCode = models.ForeignKey(CustomUser, on_delete=models.SET_NULL,null=True)
    fromDate = models.DateField(null=True,blank=True)
    toDate = models.DateField(null=True,blank=True)
    region = models.CharField(max_length=100,null=False,blank=False)
    region_code = models.CharField(max_length=100,null=False,blank=False)
    circle = models.CharField(max_length=100,null=True,blank=True)
    circle_code = models.CharField(max_length=100,null=True,blank=True)
    division = models.CharField(max_length=100,null=True,blank=True)
    division_code = models.CharField(max_length=100,null=True,blank=True)
    subdivision = models.CharField(max_length=100,null=True,blank=True)
    subdivision_code = models.CharField(max_length=100,null=True,blank=True)
    dc = models.CharField(max_length=100,null=True,blank=True)
    dc_code = models.CharField(max_length=100,null=True,blank=True)
    reportingDesignation = models.CharField(max_length=100,null=False,blank=False)
    reportingOfficerCode = models.CharField(max_length=100,null=False,blank=False)
    reportingOfficer = models.CharField(max_length=100,null=False,blank=False)
    reviewingDesignation = models.CharField(max_length=100,null=False,blank=False)
    reviewingOfficerCode = models.CharField(max_length=100,null=False,blank=False)
    reviewingOfficer = models.CharField(max_length=100,null=False,blank=False)
    acceptingDesignation = models.CharField(max_length=100,null=False,blank=False)
    acceptingOfficerCode = models.CharField(max_length=100,null=False,blank=False)
    acceptingOfficer = models.CharField(max_length=100,null=False,blank=False)
    hrManager = models.CharField(max_length=100,null=False,blank=False)
    hrManagerCode = models.CharField(max_length=100,null=False,blank=False)
    financialYear = models.CharField(max_length=100,null=False,blank=False)
    isAnotherTagging = models.BooleanField(default=False)
    isFinal = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.id)

    def save(self,*args,**kwargs):
        if not self.pk:
            self.created_at = timezone.now()
        else:
            self.updated_at = timezone.now()
        super().save(*args,**kwargs)

    # def __str__(self):
    #     return str(self.empCode) + " - " +str(self.id)

class HrManagers(models.Model):

    regionCode = models.IntegerField(null=False,blank=False)
    regionName = models.CharField(max_length=100,null=False,blank=False)
    circleCode = models.CharField(max_length=100,null=True,blank=True)
    circleName = models.CharField(max_length=100,null=True,blank=True)
    circleNameHindi = models.CharField(max_length=100,null=True,blank=True)
    empName = models.CharField(max_length=100,null=False,blank=False)
    empCode = models.CharField(max_length=100,null=False,blank=False)
    empId = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return str(self.empName)
class ACR_Session(models.Model):
    # name = models.ForeignKey(CustomUser, on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=100,null=True, blank=True)
    fromDate = models.DateField(null=True, blank=True)
    midDate = models.DateField(null=True, blank=True)
    toDate = models.DateField(null=True, blank=True)
    isActive = models.BooleanField(default=False)
    def __str__(self):
        return str(self.name)
class ACR_Dates(models.Model):
    acr_session = models.ForeignKey(ACR_Session, on_delete=models.SET_NULL,null=True)
    accepting_start_date = models.DateField(null=True, blank=True)
    accepting_end_date = models.DateField(null=True, blank=True)
    appraise_start_date = models.DateField(null=True, blank=True)
    appraise_end_date = models.DateField(null=True, blank=True)
    tagging_start_date = models.DateField(null=True, blank=True)
    tagging_end_date = models.DateField(null=True, blank=True)
    reporting_start_date = models.DateField(null=True, blank=True)
    reporting_end_date = models.DateField(null=True, blank=True)
    reviewing_start_date = models.DateField(null=True, blank=True)
    reviewing_end_date = models.DateField(null=True, blank=True)
    disclosure_date = models.DateField(null=True, blank=True)
    representation_start_date = models.DateField(null=True, blank=True)
    representation_end_date = models.DateField(null=True, blank=True)


    def __str__(self):
        return str(self.acr_session)

# Create your models here.
# Extras Code here

class ReportingOfficer(models.Model):
    tagging=models.ForeignKey(EmployeeTagging,on_delete=models.CASCADE,null=True)
    descriptions=models.CharField(max_length=1000, null=True, blank=True)
    final_grade=models.CharField(max_length=100, null=True, blank=True)
    reportingofficer_name=models.CharField(max_length=100, null=True, blank=True)
    reportingofficer_code=models.CharField(max_length=100, null=True, blank=True)
    reporting_pdf=models.FileField(upload_to="reporting_officer_pdf", null=True, blank=True)
    grade_one=models.CharField(max_length=100, null=True, blank=True)
    grade_two=models.CharField(max_length=100, null=True, blank=True)
    grade_three=models.CharField(max_length=100, null=True, blank=True)
    grade_four=models.CharField(max_length=100, null=True, blank=True)
    grade_five=models.CharField(max_length=100, null=True, blank=True)
    grade_six=models.CharField(max_length=100, null=True, blank=True)
    grade_seven=models.CharField(max_length=100, null=True, blank=True)
    grade_eight=models.CharField(max_length=100, null=True, blank=True)
    grade_nine=models.CharField(max_length=100, null=True, blank=True)
    grade_ten=models.CharField(max_length=100, null=True, blank=True)
    created_at= models.DateTimeField(null=True, blank=True,auto_now=True)
    updated_at= models.DateTimeField(null=True, blank=True,auto_now=True)
    is_Status=models.BooleanField()

    def save(self,*args,**kwargs):
        if not self.pk:
            self.created_at = timezone.now()
        else:
            self.updated_at = timezone.now()
        super().save(*args,**kwargs)

class LoginOtp(models.Model):
    emp=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    otp=models.IntegerField(null=True,blank=True)
    created_at= models.DateTimeField(null=True, blank=True,auto_now=True)
    updated_at= models.DateTimeField(null=True, blank=True,auto_now=True)

class ReviewingOfficer(models.Model):
    tagging=models.ForeignKey(EmployeeTagging,on_delete=models.CASCADE,null=True)
    descriptions=models.CharField(max_length=1000, null=True, blank=True)
    final_grade=models.CharField(max_length=100, null=True, blank=True)
    reviewing_officer_pdf=models.FileField(upload_to="reviewing_officer_pdf", null=True, blank=True)
    created_at= models.DateTimeField(null=True, blank=True,auto_now=True)
    updated_at= models.DateTimeField(null=True, blank=True,auto_now=True)
    is_Status=models.BooleanField()
        
    def save(self,*args,**kwargs):
        if not self.pk:
            self.created_at = timezone.now()
        else:
            self.updated_at = timezone.now()
        super().save(*args,**kwargs)


class AcceptingOfficer(models.Model):
    tagging=models.ForeignKey(EmployeeTagging,on_delete=models.CASCADE,null=True)
    descriptions=models.CharField(max_length=1000, null=True, blank=True)
    final_grade=models.CharField(max_length=100, null=True, blank=True)
    accepting_officer_pdf=models.FileField(upload_to="accepting_officer_pdf", null=True, blank=True)
    created_at= models.DateTimeField(null=True, blank=True,auto_now=True)
    updated_at= models.DateTimeField(null=True, blank=True,auto_now=True)
    is_Status=models.BooleanField()

    def save(self,*args,**kwargs):
        if not self.pk:
            self.created_at = timezone.now()
        else:
            self.updated_at = timezone.now()
        super().save(*args,**kwargs)