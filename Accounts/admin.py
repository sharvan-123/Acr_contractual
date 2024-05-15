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

def export_to_csv_EmployeeSelfAppraisal(modeladmin, request, queryset):
    queryset = EmployeeSelfAppraisal.objects.values("taggingId__id","empCode__empCode", "fullName", "empCode__designation__name","fromDate", "toDate", "region", "region_code", "circle", "circle_code", "division", "division_code", "subdivision", "subdivision_code", "dc", "dc_code", "reportingDesignation", "reportingOfficerCode", "reportingOfficer", "isStatus").distinct()
    response = ExcelResponse(queryset)
    response['Content-Disposition'] = 'attachment; filename="EmployeeSelfAppraisal.xlsx"'
    return response

export_to_csv_EmployeeSelfAppraisal.short_description = 'Export All Data'

class HrManagersAdmin(admin.ModelAdmin):
    list_display = ('empCode', 'empName', 'regionName', 'circleName')
    search_fields = ('empCode', 'empName', 'regionName', 'circleName')
    actions = [export_to_csv_HrManagers]


class EmployeeTaggingAdmin(admin.ModelAdmin):
    list_display = ('id', 'empCode', 'fromDate', 'toDate', 'reportingOfficer', 'reviewingOfficer', 'acceptingOfficer', 'hrManager', 'isAnotherTagging', 'isFinal')
    search_fields = ('id', 'empCode__empCode', 'reportingOfficer', 'reviewingOfficer', 'acceptingOfficer', 'hrManager')
    actions = [export_to_csv_EmployeeTagging]
class EmployeeSelfAppraisalAdmin(admin.ModelAdmin):
    list_display = ('id', 'taggingId', 'empCode', 'fullName', 'region', 'circle', 'fromDate', 'toDate', 'reportingOfficer', 'isStatus',)
    search_fields = ('taggingId__id', 'empCode__empCode', 'fullName', 'reportingOfficer', 'fullName')
    list_filter = ("reportingOfficer",)
    actions = [export_to_csv_EmployeeSelfAppraisal]

class EmployeeReportingAdmin(admin.ModelAdmin):
    list_display = ('id', 'taggingId', 'taggingId_full_name', 'reportingOfficerCode', 'reporting_officer_code_full_name', 'updated_at', 'isStatus',)
    search_fields = ('taggingId__id', 'taggingId__empCode__fullName', 'reportingOfficerCode__empCode', 'reportingOfficerCode__fullName',)

    def reporting_officer_code_full_name(self, obj):
        return obj.reportingOfficerCode.fullName if obj.reportingOfficerCode else None

    reporting_officer_code_full_name.short_description = 'Reporting Officer Full Name'
    def taggingId_full_name(self, obj):
        return obj.taggingId.empCode.fullName if obj.taggingId else None

    taggingId_full_name.short_description = 'Tagging User Full Name'


class EmployeeReportingClass3Admin(admin.ModelAdmin):
    list_display = ('id', 'taggingId', 'reportingOfficerCode', 'empNumber', 'fullName', 'dateOfBirth', 'designation', 'updated_at', 'isStatus',)
    search_fields = ('taggingId__id', 'empNumber', 'fullName', 'reportingOfficerCode__empCode', 'reportingOfficerCode__fullName','fullName',)


class EmployeeReviewingAdmin(admin.ModelAdmin):
    list_display = ('id', 'taggingId', 'taggingId_full_name', 'reviewingOfficerCode', 'reviewing_officer_code_full_name', 'updated_at', 'isStatus',)
    search_fields = ('taggingId__id', 'reviewingOfficerCode__empCode', 'reviewingOfficerCode__fullName',)

    def reviewing_officer_code_full_name(self, obj):
        return obj.reviewingOfficerCode.fullName if obj.reviewingOfficerCode else None

    reviewing_officer_code_full_name.short_description = 'Reviewing Officer Full Name'
    def taggingId_full_name(self, obj):
        return obj.taggingId.empCode.fullName if obj.taggingId else None

    taggingId_full_name.short_description = 'Tagging User Full Name'

class EmployeeReviewingClass3Admin(admin.ModelAdmin):
    list_display = ('id', 'taggingId', 'taggingId_full_name', 'reviewingOfficerCode', 'reviewing_officer_code_full_name', 'updated_at', 'isStatus',)
    search_fields = ('taggingId__id', 'reviewingOfficerCode__empCode', 'reviewingOfficerCode__fullName')

    def reviewing_officer_code_full_name(self, obj):
        return obj.reviewingOfficerCode.fullName if obj.reviewingOfficerCode else None

    reviewing_officer_code_full_name.short_description = 'Reviewing Officer Full Name'
    def taggingId_full_name(self, obj):
        return obj.taggingId.empCode.fullName if obj.taggingId else None

    taggingId_full_name.short_description = 'Tagging User Full Name'

class EmployeeAcceptingAdmin(admin.ModelAdmin):
    list_display = ('id', 'taggingId', 'taggingId_full_name', 'acceptingOfficerCode', 'accepting_officer_code_full_name', 'updated_at', 'isStatus',)
    search_fields = ('taggingId__id', 'acceptingOfficerCode__empCode', 'acceptingOfficerCode__fullName')

    def accepting_officer_code_full_name(self, obj):
        return obj.acceptingOfficerCode.fullName if obj.acceptingOfficerCode else None

    accepting_officer_code_full_name.short_description = 'Accepting Officer Full Name'
    def taggingId_full_name(self, obj):
        return obj.taggingId.empCode.fullName if obj.taggingId else None

    taggingId_full_name.short_description = 'Tagging User Full Name'


class kpiMtrAdmin(admin.ModelAdmin):
    list_display = ('kpiId', 'level', 'name', 'code', 'loc_code', 'bill_month', 'tot_defmtrs', 'per_assessment_billing', 'tot_mtr_cons', 'mtr_cons_per', 'unmtr_cons', 'unmtr_cons_per', 'billing_efficiency', 'collection_efficiency', 'atc', 'input', 'collection', 'crpu', 'fdr_count', 'avg_supply', 'kpi_agri_shms_avg', 'tot_dtr_mar21', 'failed_dtr', 'fail_per_mar21', 'tot_dtrs', 'total_fail_dtr', 'fail_per_dtr', 'tot_consumer', 'amr_consumer', 'per_amr', 'kpi_nonagr_fdr_count', 'kpi_nonagr_avg_supply', 'kpi_nonagr_avg', 'flat_rate_per_paid_cd', 'flat_rate_per_paid_bn', 'kpi_temp_cons_count_nsc',)
    search_fields = ('name', 'code', 'level', 'loc_code',)
    list_filter = ('level', 'bill_month', 'name',)

class kpiAdmin(admin.ModelAdmin):
    list_display = ("fun_name", "kpi_name")
    search_fields = ("kpi_name",)
    list_filter = ("fun_name",)
class kpiFunctionAdmin(admin.ModelAdmin):
    list_display = ("fun_name", "fun_code")
    search_fields = ("fun_name",)
    list_filter = ("fun_name",)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(EmployeeTagging, EmployeeTaggingAdmin)
admin.site.register(HrManagers, HrManagersAdmin)
admin.site.register(ACR_Session)
admin.site.register(ACR_Dates)
admin.site.register(ReportingOfficer)

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
