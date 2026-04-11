from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import Q
from django.http import HttpResponse
from excel_response import ExcelResponse
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *
import csv


class JSONFieldKeyListFilter(admin.SimpleListFilter):
    title = 'Employment Type'
    parameter_name = 'employment_type'

    def lookups(self, request, model_admin):
        queryset = model_admin.get_queryset(request)
        values_list = queryset.values_list('employmentType__name', flat=True).order_by('empCode').distinct()
        return [(value, value) for value in values_list]

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(employmentType__name=value)
        else:
            return queryset
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('empCode', 'fullName', 'email', 'mobileNo', 'employmentType', 'is_staff', 'is_active',)
    fieldsets = (
        ("Details", {'fields': ('empCode', 'firstName', 'middleName', 'lastName', 'fullName', 'mobileNo',
                                'aadhaarNumber', 'dateOfBirth', 'dateOfJoining', 'dateOfTraining', 'gender',
                                'fatherName', 'motherName', 'maritalStatus', 'heightOfEmployee',
                                'personalIdentificationMark', 'physicallyHandicaped', 'percentageOfDisablement',
                                'employmentType', 'category', 'email', 'address', 'city', 'region', 'circle',
                                'division', 'subDivision', 'dc', 'substation', 'defaultShift', 'designation',
                                'reportingOfficer', 'reportingOfficerDesignation', 'bankName', 'bankAccount',
                                'bankIfsc', 'isReportingOfficer', 'isManagerHr', 'isAeIt', 'isScnIssuer',
                                'isTransferOrderApprover', 'isCurrentCharge', 'currentChargeDesignation',
                                'dateOfCurrentCharge', 'dateOfRegularisation', 'managerHr', 'panNo', 'managerHrName',
                                'attendanceLocationId', 'departmentId', 'stateOfBirth', 'townOrCityOfBirth',
                                'isRegisteredHandicapped', 'discriptionOfHandicapped', 'officialEmail', 'gsliNumber',
                                'bloodGroup', 'correspondenceAddress', 'basicPay', 'providentFundType', 'pranNumber',
                                'pfNumber', 'holidayList', 'deviceId', 'otpSecretKey', 'otpCounter', 'status',)}),

        ('Permissions', {'fields': ('is_login','is_staff','is_active','groups', 'user_permissions',)
                         }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('empCode', 'email', 'fullName', 'mobileNo', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('empCode', 'fullName', 'email', 'mobileNo', 'employmentType',)
    list_filter = (JSONFieldKeyListFilter,)
    ordering = ('empCode',)

def export_to_csv_HrManagers(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="HrManger.csv"'
    writer = csv.writer(response)
    writer.writerow(['id', 'regionCode', 'regionName', 'circleCode', 'circleName', 'circleNameHindi', 'empName', 'empCode', 'empId'])
    for obj in queryset:writer.writerow([obj.id, obj.regionCode, obj.regionName, obj.circleCode, obj.circleName, obj.circleNameHindi, obj.empName, obj.empCode, obj.empId])
    return response
export_to_csv_HrManagers.short_description = 'Export to CSV'

def export_to_csv_EmployeeTagging(modeladmin, request, queryset):
    queryset = EmployeeTagging.objects.values("id", "empCode__empCode", "empCode__fullName", "empCode__designation__name","fromDate", "toDate", "region", "region_code", "circle", "circle_code", "division", "division_code", "subdivision", "subdivision_code", "dc", "dc_code", "reportingDesignation", "reportingOfficerCode", "reportingOfficer", "reviewingDesignation", "reviewingOfficerCode", "reviewingOfficer", "acceptingDesignation", "acceptingOfficerCode", "acceptingOfficer", "hrManager", "hrManagerCode", "financialYear", "isAnotherTagging", "isFinal").distinct()
    response = ExcelResponse(queryset)
    response['Content-Disposition'] = 'attachment; filename="EmployeeTagging.xlsx"'
    return response

export_to_csv_EmployeeTagging.short_description = 'Export All Data'

class HrManagersAdmin(admin.ModelAdmin):
    list_display = ('empCode', 'empName', 'regionName', 'circleName')
    search_fields = ('empCode', 'empName', 'regionName', 'circleName')
    actions = [export_to_csv_HrManagers]


class EmployeeTaggingAdmin(admin.ModelAdmin):
    list_display = ('id', 'empCode', 'fromDate', 'toDate', 'reportingOfficer', 'reviewingOfficer', 'acceptingOfficer', 'hrManager', 'isAnotherTagging', 'isFinal')
    search_fields = ('id', 'empCode__empCode', 'reportingOfficer', 'reviewingOfficer', 'acceptingOfficer', 'hrManager')
    actions = [export_to_csv_EmployeeTagging]

def download_excel(request, type):
    try:
        Session = ACR_Session.objects.filter(isActive=True)[0]
        if type == 'tagging':
            taggingUser = EmployeeTagging.objects.filter(financialYear=Session).values_list('empCode', flat=True).distinct()
            queryset = CustomUser.objects.filter(employmentType__empTypeId__in=[1,5,7,9]).filter(status="Active").filter(designation__designationClass__in=["1","2","3"]).exclude(id__in=taggingUser).values("empCode", "fullName", "region__name", "circle__name", "division__name", "subDivision__name", "dc__name",)
        response = ExcelResponse(queryset)
        response['Content-Disposition'] = 'attachment; filename="filtered_data.xlsx"'
    except:
        response = 'Something went wrong'
    return response


@admin.register(ReportingOfficer)
class ReportingOfficerAdmin(admin.ModelAdmin):
    list_display = ('id','tagging','reportingofficer_name','final_grade','is_Status','created_at')
    search_fields = ('reportingofficer_name','final_grade')
    list_filter = ('is_Status','created_at')
    readonly_fields = ('created_at','updated_at')


@admin.register(ReviewingOfficer)
class ReviewingOfficerAdmin(admin.ModelAdmin):
    list_display = ('id','tagging','final_grade','is_Status','created_at')
    search_fields = ('final_grade',)
    list_filter = ('is_Status','created_at')
    readonly_fields = ('created_at','updated_at')


@admin.register(AcceptingOfficer)
class AcceptingOfficerAdmin(admin.ModelAdmin):
    list_display = ('id','tagging','final_grade','is_Status','created_at')
    search_fields = ('final_grade',)
    list_filter = ('is_Status','created_at')
    readonly_fields = ('created_at','updated_at')


@admin.register(LoginOtp)
class LoginOtpAdmin(admin.ModelAdmin):
    list_display = ('id','emp','otp','created_at')
    search_fields = ('emp__username','otp')
    readonly_fields = ('created_at','updated_at')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(EmployeeTagging, EmployeeTaggingAdmin)
admin.site.register(HrManagers, HrManagersAdmin)