from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.db.models.functions import Concat
from django.db.models import Value
from datetime import date
from django import forms
from .models import *

OPTIONS = [('YES', 'YES'),('NO', 'NO'),]
class EmployeeTaggingForm(forms.ModelForm):
    taggingUser = EmployeeTagging.objects.values_list('empCode', flat=True).distinct()
    full_name_expression = Concat('empCode', Value(' - '), 'fullName')
    empCode = forms.ModelChoiceField(queryset=CustomUser.objects.exclude(id__in=taggingUser), to_field_name="empCode", empty_label="Select Empolyee", widget=forms.Select(attrs={'tabindex':'-1', 'class':'select2-hidden-accessible', 'aria-hidden':'true', 'id': 'inputEmpCode'}), required=False)
    fromDate = forms.DateField(label='From Date', widget=forms.TextInput(attrs={'class': 'form-control ', 'type': 'date', 'id': 'inputFromDate', 'placeholder': 'Select From-Date', 'autocomplete':'off',}), required=True)
    toDate = forms.DateField(label='To Date', widget=forms.TextInput(attrs={'class': 'form-control ', 'type': 'date', 'id': 'inputToDate', 'placeholder': 'Select To-Date','autocomplete': 'off', 'disabled': True}), required=True)
    region_code = forms.CharField(label='Region', widget=forms.Select(choices=(('', 'Select Region...'),), attrs={'class': 'form-control', 'id': 'inputRegion', }), required=True)
    region = forms.CharField(label='Region Code', widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'inputRegionVal'}))
    circle_code = forms.CharField(label='Circle', widget=forms.Select(choices=(('', 'Select Circle...'),), attrs={'class': 'form-control', 'id': 'inputCircle', 'disabled': True}), required=False)
    circle = forms.CharField(label='Region Code', widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'inputCircleVal'}), required=False)
    division_code = forms.CharField(label='Division', widget=forms.Select(choices=(('', 'Select Division...'),), attrs={'class': 'form-control', 'id': 'inputDivision', 'disabled': True}), required=False)
    division = forms.CharField(label='Region Code', widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'inputDivisionVal'}), required=False)
    subdivision_code = forms.CharField(label='SubDivision', widget=forms.Select(choices=(('', 'Select SubDivision...'),), attrs={'class': 'form-control', 'id': 'inputSubDivision', 'disabled': True}), required=False)
    subdivision = forms.CharField(label='Region Code', widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'inputSubDivisionVal'}), required=False)
    dc_code = forms.CharField(label='DC', widget=forms.Select(choices=(('', 'Select DC...'),), attrs={'class': 'form-control', 'id': 'inputDC', 'disabled': True}), required=False)
    dc = forms.CharField(label='Region Code', widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'inputDCVal'}), required=False)
    reportingDesignation = forms.CharField(label='Designation', widget=forms.Select(choices=(('', 'Select Designation...'),), attrs={'class': 'form-control', 'id': 'inputReportingDesignation',}), required=True)
    reportingOfficer = forms.CharField(label='Region Code', widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'inputReportingOfficerVal'}))
    reportingOfficerCode = forms.CharField(label='Officer', widget=forms.Select(choices=(('', 'Select Officer...'),), attrs={'class': 'form-control', 'id': 'inputReportingOfficer', 'disabled': True}), required=False)
    reviewingDesignation = forms.CharField(label='Designation', widget=forms.Select(choices=(('', 'Select Designation...'),), attrs={'class': 'form-control', 'id': 'inputReviewingDesignation',}), required=True)
    reviewingOfficer = forms.CharField(label='Region Code', widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'inputReviewingVal'}))
    reviewingOfficerCode = forms.CharField(label='Officer', widget=forms.Select(choices=(('', 'Select Officer...'),), attrs={'class': 'form-control', 'id': 'inputReviewing', 'disabled': True}), required=False)
    acceptingDesignation = forms.CharField(label='Designation', widget=forms.Select(choices=(('', 'Select Designation...'),), attrs={'class': 'form-control', 'id': 'inputAcceptingDesignation',}), required=True)
    acceptingOfficer = forms.CharField(label='Region Code', widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'inputAcceptingOfficerVal'}))
    acceptingOfficerCode = forms.CharField(label='Officer', widget=forms.Select(choices=(('', 'Select Officer...'),), attrs={'class': 'form-control', 'id': 'inputAcceptingOfficer','disabled': True}), required=False)
    hrManager = forms.CharField(label='Region Code', widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'inputhrManagerVal'}))
    hrManagerCode = forms.CharField(label='Region Code', widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'inputhrManager'}))
    financialYear = forms.CharField(label='Financial Year', widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'financialYear'}))
    isAnotherTagging = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-control', 'id': 'isAnotherTagging',}), required=False)

    fromDate2 = forms.DateField(label='From Date', widget=forms.TextInput(attrs={'class': 'form-control ', 'type': 'date', 'id': 'inputFromDate2', 'placeholder': 'Select From-Date', 'autocomplete':'off',}), required=False)
    toDate2 = forms.DateField(label='To Date', widget=forms.TextInput(attrs={'class': 'form-control ', 'type': 'date', 'id': 'inputToDate2', 'placeholder': 'Select To-Date','autocomplete': 'off', 'disabled': True}), required=False)
    region_code2 = forms.CharField(label='Region', widget=forms.Select(choices=(('', 'Select Region...'),), attrs={'class': 'form-control', 'id': 'inputRegion2', }), required=False)
    region2 = forms.CharField(label='Region Code', widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'inputRegionVal2'}), required=False)
    circle_code2 = forms.CharField(label='Circle', widget=forms.Select(choices=(('', 'Select Circle...'),), attrs={'class': 'form-control', 'id': 'inputCircle2', 'disabled': True}), required=False)
    circle2 = forms.CharField(label='Region Code', widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'inputCircleVal2'}), required=False)
    division_code2 = forms.CharField(label='Division', widget=forms.Select(choices=(('', 'Select Division...'),), attrs={'class': 'form-control', 'id': 'inputDivision2', 'disabled': True}), required=False)
    division2 = forms.CharField(label='Region Code', widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'inputDivisionVal2'}), required=False)
    subdivision_code2 = forms.CharField(label='SubDivision', widget=forms.Select(choices=(('', 'Select SubDivision...'),), attrs={'class': 'form-control', 'id': 'inputSubDivision2', 'disabled': True}), required=False)
    subdivision2 = forms.CharField(label='Region Code', widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'inputSubDivisionVal2'}), required=False)
    dc_code2 = forms.CharField(label='DC', widget=forms.Select(choices=(('', 'Select DC...'),), attrs={'class': 'form-control', 'id': 'inputDC2', 'disabled': True}), required=False)
    dc2 = forms.CharField(label='Region Code', widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'inputDCVal2'}), required=False)
    reportingDesignation2 = forms.CharField(label='Designation', widget=forms.Select(choices=(('', 'Select Designation...'),), attrs={'class': 'form-control', 'id': 'inputReportingDesignation2',}), required=False)
    reportingOfficer2 = forms.CharField(label='Region Code', widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'inputReportingOfficerVal2'}), required=False)
    reportingOfficerCode2 = forms.CharField(label='Officer', widget=forms.Select(choices=(('', 'Select Officer...'),), attrs={'class': 'form-control', 'id': 'inputReportingOfficer2', 'disabled': True}), required=False)
    reviewingDesignation2 = forms.CharField(label='Designation', widget=forms.Select(choices=(('', 'Select Designation...'),), attrs={'class': 'form-control', 'id': 'inputReviewingDesignation2',}), required=False)
    reviewingOfficer2 = forms.CharField(label='Region Code', widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'inputReviewingVal2'}), required=False)
    reviewingOfficerCode2 = forms.CharField(label='Officer', widget=forms.Select(choices=(('', 'Select Officer...'),), attrs={'class': 'form-control', 'id': 'inputReviewing2', 'disabled': True}), required=False)
    acceptingDesignation2 = forms.CharField(label='Designation', widget=forms.Select(choices=(('', 'Select Designation...'),), attrs={'class': 'form-control', 'id': 'inputAcceptingDesignation2',}), required=False)
    acceptingOfficer2 = forms.CharField(label='Region Code', widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'inputAcceptingOfficerVal2'}), required=False)
    acceptingOfficerCode2 = forms.CharField(label='Officer', widget=forms.Select(choices=(('', 'Select Officer...'),), attrs={'class': 'form-control', 'id': 'inputAcceptingOfficer2','disabled': True}), required=False)
    hrManager2 = forms.CharField(label='Region Code', widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'inputhrManagerVal2'}), required=False)
    hrManagerCode2 = forms.CharField(label='Region Code', widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'inputhrManager2'}), required=False)
    financialYear2 = forms.CharField(label='Financial Year', widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'financialYear2'}), required=False)

    class Meta:
        model = EmployeeTagging
        fields = ('fromDate', 'toDate', 'region', 'region_code', 'circle', 'circle_code', 'division', 'division_code', 'subdivision', 'subdivision_code', 'dc', 'dc_code', 'reportingDesignation', 'reportingOfficerCode', 'reportingOfficer', 'reviewingDesignation', 'reviewingOfficerCode', 'reviewingOfficer', 'acceptingDesignation', 'acceptingOfficerCode', 'acceptingOfficer', 'hrManager', 'hrManagerCode', 'financialYear', 'isAnotherTagging',)


class EmployeeTaggingUpdateForm(forms.ModelForm):
    fromDate = forms.DateField(label='From Date', widget=forms.TextInput(attrs={'class': 'form-control ', 'type': 'date', 'id': 'inputFromDate', 'placeholder': 'Select From-Date', 'autocomplete':'off',}), required=True)
    toDate = forms.DateField(label='To Date', widget=forms.TextInput(attrs={'class': 'form-control ', 'type': 'date', 'id': 'inputToDate', 'placeholder': 'Select To-Date','autocomplete': 'off', 'disabled': True}), required=True)

    region = forms.CharField(label='Region Code', widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'inputRegionVal'}))
    region_code = forms.CharField(label='Region', widget=forms.Select(choices=(('', 'Select Region...'),),attrs={'class': 'form-control','id': 'inputRegion', }), required=True)
    circle = forms.CharField(label='Region Code', widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'inputCircleVal'}), required=False)
    division = forms.CharField(label='Region Code', widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'inputDivisionVal'}), required=False)
    subdivision = forms.CharField(label='Region Code', widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'inputSubDivisionVal'}), required=False)
    dc = forms.CharField(label='Region Code', widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'inputDCVal'}), required=False)

    reportingDesignation = forms.CharField(label='Designation', widget=forms.Select(choices=(('', 'Select Designation...'),), attrs={'class': 'form-control', 'id': 'inputReportingDesignation',}), required=True)
    reportingOfficer = forms.CharField(label='Region Code', widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'inputReportingOfficerVal'}))
    reportingOfficerCode = forms.CharField(label='Officer', widget=forms.Select(choices=(('', 'Select Officer...'),), attrs={'class': 'form-control', 'id': 'inputReportingOfficer', 'disabled': True}), required=False)
    reviewingDesignation = forms.CharField(label='Designation', widget=forms.Select(choices=(('', 'Select Designation...'),), attrs={'class': 'form-control', 'id': 'inputReviewingDesignation',}), required=True)
    reviewingOfficer = forms.CharField(label='Region Code', widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'inputReviewingVal'}))
    reviewingOfficerCode = forms.CharField(label='Officer', widget=forms.Select(choices=(('', 'Select Officer...'),), attrs={'class': 'form-control', 'id': 'inputReviewing', 'disabled': True}), required=False)
    acceptingDesignation = forms.CharField(label='Designation', widget=forms.Select(choices=(('', 'Select Designation...'),), attrs={'class': 'form-control', 'id': 'inputAcceptingDesignation',}), required=True)
    acceptingOfficer = forms.CharField(label='Region Code', widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'inputAcceptingOfficerVal'}))
    acceptingOfficerCode = forms.CharField(label='Officer', widget=forms.Select(choices=(('', 'Select Officer...'),), attrs={'class': 'form-control', 'id': 'inputAcceptingOfficer','disabled': True}), required=False)
    hrManager = forms.CharField(label='Region Code', widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'inputhrManagerVal'}))
    hrManagerCode = forms.CharField(label='Region Code', widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'inputhrManager'}))
    financialYear = forms.CharField(label='Financial Year', widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'financialYear'}))
    isAnotherTagging = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-control', 'id': 'isAnotherTagging',}), required=False)

    class Meta:
        model = EmployeeTagging
        fields = ('fromDate', 'toDate', 'region', 'region_code', 'circle', 'circle_code', 'division', 'division_code', 'subdivision', 'subdivision_code', 'dc', 'dc_code', 'reportingDesignation', 'reportingOfficerCode', 'reportingOfficer', 'reviewingDesignation', 'reviewingOfficerCode', 'reviewingOfficer', 'acceptingDesignation', 'acceptingOfficerCode', 'acceptingOfficer', 'hrManager', 'hrManagerCode', 'financialYear', 'isAnotherTagging',)


class CustomUserCreationForm(UserCreationForm):
    email = forms.CharField(label="Email",widget=forms.TextInput(attrs={'class':'form-group'}))
    mobile = forms.CharField(label="Mobile",widget=forms.HiddenInput(attrs={'class':'form-group', 'type':'number'}))
    role = forms.CharField(label="",widget=forms.HiddenInput(attrs={'class':'form-group', 'value':'Retailer'}))
    parent_detail = forms.CharField(label="",widget=forms.HiddenInput(attrs={'class':'form-group', 'value':'Admin'}))
    pincode = forms.CharField(label="Pincode",widget=forms.HiddenInput(attrs={'class':'form-group', 'type':'number'}))
    class Meta:
        model = CustomUser
        fields = ('empCode', 'fullName', 'mobileNo', 'aadhaarNumber', 'dateOfBirth', 'dateOfJoining', 'gender',
                  'employmentType','category', 'email', 'address', 'city', 'reportingOfficer')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        # fields = ('email', 'mobile', 'pan',)
        fields = ('empCode', 'fullName', 'mobileNo', 'aadhaarNumber', 'dateOfBirth', 'dateOfJoining', 'gender',
                  'employmentType','category', 'email', 'address', 'city', 'reportingOfficer')


#Extras