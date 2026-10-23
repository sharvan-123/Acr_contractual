import csv

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponse
from excel_response import ExcelResponse

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import (
    CustomUser,
    EmployeeTagging,
    HrManagers,
    ReportingOfficer,
    ReviewingOfficer,
    AcceptingOfficer,
    LoginOtp,
    ACR_Session,
    ACR_Dates,
)


class JSONFieldKeyListFilter(admin.SimpleListFilter):
    """Filter users by the employment type stored in the JSON field."""
    title = "Employment Type"
    parameter_name = "employment_type"

    def lookups(self, request, model_admin):
        values = set()
        for item in model_admin.get_queryset(request).values_list(
            "employmentType", flat=True
        ):
            if isinstance(item, dict):
                value = item.get("name")
                if value:
                    values.add(str(value))
            elif isinstance(item, list):
                for entry in item:
                    if isinstance(entry, dict) and entry.get("name"):
                        values.add(str(entry["name"]))
                    elif entry:
                        values.add(str(entry))
            elif item:
                values.add(str(item))
        return [(value, value) for value in sorted(values)]

    def queryset(self, request, queryset):
        value = self.value()
        if not value:
            return queryset
        # JSONField key lookup; supports the common {"name": "..."} structure.
        return queryset.filter(employmentType__name=value)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = (
        "empCode", "fullName", "email", "mobileNo",
        "employmentType", "is_staff", "is_active",
    )
    list_display_links = ("empCode", "fullName")
    search_fields = (
        "empCode", "empId", "fullName", "firstName", "middleName",
        "lastName", "email", "mobileNo", "officialEmail",
    )
    list_filter = (
        JSONFieldKeyListFilter, "is_staff", "is_active", "status",
        "isReportingOfficer", "isManagerHr",
    )
    ordering = ("empCode",)
    list_per_page = 50

    fieldsets = (
        ("Details", {
            "fields": (
                "empCode", "empId", "firstName", "middleName", "lastName",
                "fullName", "mobileNo", "aadhaarNumber", "dateOfBirth",
                "dateOfJoining", "dateOfTraining", "gender", "fatherName",
                "motherName", "maritalStatus", "heightOfEmployee",
                "personalIdentificationMark", "physicallyHandicaped",
                "percentageOfDisablement", "employmentType", "category",
                "email", "address", "city", "region", "circle", "division",
                "subDivision", "dc", "substation", "defaultShift",
                "designation", "reportingOfficer", "reportingOfficerDesignation",
                "bankName", "bankAccount", "bankIfsc", "isReportingOfficer",
                "isManagerHr", "isAeIt", "isScnIssuer",
                "isTransferOrderApprover", "isCurrentCharge",
                "currentChargeDesignation", "dateOfCurrentCharge",
                "dateOfRegularisation", "managerHr", "panNo", "managerHrName",
                "attendanceLocationId", "departmentId", "stateOfBirth",
                "townOrCityOfBirth", "isRegisteredHandicapped",
                "discriptionOfHandicapped", "officialEmail", "gsliNumber",
                "bloodGroup", "correspondenceAddress", "basicPay",
                "providentFundType", "pranNumber", "pfNumber", "holidayList",
                "deviceId", "otpSecretKey", "otpCounter", "status",
            )
        }),
        ("Permissions", {
            "fields": (
                "is_login", "is_staff", "is_active", "groups",
                "user_permissions",
            )
        }),
        ("Dates", {"fields": ("date_joined", "created_at", "updated_at")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "empCode", "empId", "email", "fullName", "mobileNo",
                "password1", "password2", "is_staff", "is_active",
            ),
        }),
    )
    readonly_fields = ("date_joined", "created_at", "updated_at")


def export_to_csv_HrManagers(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="HrManagers.csv"'
    writer = csv.writer(response)
    writer.writerow([
        "id", "regionCode", "regionName", "circleCode", "circleName",
        "circleNameHindi", "empName", "empCode", "empId",
    ])
    for obj in queryset:
        writer.writerow([
            obj.id, obj.regionCode, obj.regionName, obj.circleCode,
            obj.circleName, obj.circleNameHindi, obj.empName, obj.empCode,
            obj.empId,
        ])
    return response


export_to_csv_HrManagers.short_description = "Export selected HR Managers to CSV"


def export_to_csv_EmployeeTagging(modeladmin, request, queryset):
    rows = queryset.values(
        "id", "empCode__empCode", "empCode__fullName",
        "empCode__designation", "fromDate", "toDate", "region",
        "region_code", "circle", "circle_code", "division", "division_code",
        "subdivision", "subdivision_code", "dc", "dc_code",
        "reportingDesignation", "reportingOfficerCode", "reportingOfficer",
        "reviewingDesignation", "reviewingOfficerCode", "reviewingOfficer",
        "acceptingDesignation", "acceptingOfficerCode", "acceptingOfficer",
        "hrManager", "hrManagerCode", "financialYear", "isAnotherTagging",
        "isFinal",
    ).distinct()
    response = ExcelResponse(rows)
    response["Content-Disposition"] = 'attachment; filename="EmployeeTagging.xlsx"'
    return response


export_to_csv_EmployeeTagging.short_description = "Export selected tagging to Excel"


@admin.register(EmployeeTagging)
class EmployeeTaggingAdmin(admin.ModelAdmin):
    list_display = (
        "id", "employee_code", "employee_name", "fromDate", "toDate",
        "financialYear", "region", "circle", "division", "subdivision", "dc",
        "reportingOfficerCode", "reportingOfficer",
        "reviewingOfficerCode", "reviewingOfficer",
        "acceptingOfficerCode", "acceptingOfficer",
        "hrManagerCode", "hrManager", "isAnotherTagging", "isFinal",
    )
    list_display_links = ("id", "employee_code")
    search_fields = (
        "id", "empCode__empCode", "empCode__empId", "empCode__fullName",
        "empCode__firstName", "empCode__lastName",
        "region", "region_code", "circle", "circle_code",
        "division", "division_code", "subdivision", "subdivision_code",
        "dc", "dc_code",
        "reportingDesignation", "reportingOfficerCode", "reportingOfficer",
        "reviewingDesignation", "reviewingOfficerCode", "reviewingOfficer",
        "acceptingDesignation", "acceptingOfficerCode", "acceptingOfficer",
        "hrManager", "hrManagerCode", "financialYear",
    )
    list_filter = (
        "financialYear", "fromDate", "toDate", "region", "circle",
        "division", "subdivision", "dc", "isAnotherTagging", "isFinal",
    )
    autocomplete_fields = ("empCode",)
    list_select_related = ("empCode",)
    date_hierarchy = "fromDate"
    ordering = ("-id",)
    list_per_page = 50
    actions = (export_to_csv_EmployeeTagging,)

    @admin.display(description="Employee Code", ordering="empCode__empCode")
    def employee_code(self, obj):
        return obj.empCode.empCode if obj.empCode else "-"

    @admin.display(description="Employee Name", ordering="empCode__fullName")
    def employee_name(self, obj):
        return obj.empCode.fullName if obj.empCode else "-"


@admin.register(HrManagers)
class HrManagersAdmin(admin.ModelAdmin):
    list_display = (
        "empCode", "empName", "regionCode", "regionName",
        "circleCode", "circleName", "empId",
    )
    search_fields = (
        "empCode", "empName", "empId", "regionCode", "regionName",
        "circleCode", "circleName", "circleNameHindi",
    )
    list_filter = ("regionName", "circleName")
    ordering = ("empName",)
    list_per_page = 50
    actions = (export_to_csv_HrManagers,)


class TaggingOfficerAdminBase(admin.ModelAdmin):
    list_display = (
        "id", "tagging", "employee_code", "employee_name",
        "employee_financial_year", "final_grade", "is_Status",
        "isAutoForward", "empType", "created_at",
    )
    list_display_links = ("id", "tagging")
    search_fields = (
        "tagging__id", "tagging__empCode__empCode",
        "tagging__empCode__fullName", "tagging__financialYear",
        "tagging__reportingOfficer", "tagging__reportingOfficerCode",
        "tagging__reviewingOfficer", "tagging__reviewingOfficerCode",
        "tagging__acceptingOfficer", "tagging__acceptingOfficerCode",
        "final_grade",
    )
    list_filter = (
        "is_Status", "isAutoForward", "empType", "created_at",
        "tagging__financialYear", "tagging__isFinal",
        "tagging__isAnotherTagging",
    )
    autocomplete_fields = ("tagging",)
    list_select_related = ("tagging", "tagging__empCode")
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    list_per_page = 50

    @admin.display(description="Employee Code")
    def employee_code(self, obj):
        return obj.tagging.empCode.empCode if obj.tagging and obj.tagging.empCode else "-"

    @admin.display(description="Employee Name")
    def employee_name(self, obj):
        return obj.tagging.empCode.fullName if obj.tagging and obj.tagging.empCode else "-"

    @admin.display(description="Financial Year")
    def employee_financial_year(self, obj):
        return obj.tagging.financialYear if obj.tagging else "-"


@admin.register(ReportingOfficer)
class ReportingOfficerAdmin(TaggingOfficerAdminBase):
    list_display = TaggingOfficerAdminBase.list_display + (
        "reportingofficer_name", "reportingofficer_code",
    )
    search_fields = TaggingOfficerAdminBase.search_fields + (
        "reportingofficer_name", "reportingofficer_code",
    )


@admin.register(ReviewingOfficer)
class ReviewingOfficerAdmin(TaggingOfficerAdminBase):
    pass


@admin.register(AcceptingOfficer)
class AcceptingOfficerAdmin(TaggingOfficerAdminBase):
    pass


@admin.register(LoginOtp)
class LoginOtpAdmin(admin.ModelAdmin):
    list_display = ("id", "emp", "otp", "created_at")
    search_fields = ("emp__empCode", "emp__fullName", "otp")
    list_filter = ("created_at",)
    autocomplete_fields = ("emp",)
    list_select_related = ("emp",)
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 50


@admin.register(ACR_Session)
class ACRSessionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "fromDate", "midDate", "toDate", "isActive")
    search_fields = ("name",)
    list_filter = ("isActive", "fromDate", "toDate")
    ordering = ("-fromDate",)


@admin.register(ACR_Dates)
class ACRDatesAdmin(admin.ModelAdmin):
    list_display = (
        "id", "acr_session", "accepting_start_date", "accepting_end_date",
        "appraise_start_date", "appraise_end_date", "tagging_start_date",
        "tagging_end_date", "reporting_start_date", "reporting_end_date",
        "reviewing_start_date", "reviewing_end_date", "disclosure_date",
    )
    search_fields = ("acr_session__name",)
    list_filter = ("acr_session", "tagging_start_date", "reporting_start_date",
                   "reviewing_start_date", "accepting_start_date")
    autocomplete_fields = ("acr_session",)
    list_select_related = ("acr_session",)
    list_per_page = 50


def download_excel(request, type):
    try:
        session = ACR_Session.objects.filter(isActive=True).first()
        if not session:
            return HttpResponse("No active ACR session found.", status=404)

        if type == "tagging":
            tagged_employee_ids = EmployeeTagging.objects.filter(
                financialYear=session
            ).values_list("empCode", flat=True).distinct()
            queryset = CustomUser.objects.filter(
                employmentType__empTypeId__in=[1, 5, 7, 9],
                status="Active",
                designation__designationClass__in=["1", "2", "3"],
            ).exclude(id__in=tagged_employee_ids).values(
                "empCode", "fullName", "region", "circle", "division",
                "subDivision", "dc",
            )
        else:
            return HttpResponse("Invalid download type.", status=400)

        response = ExcelResponse(queryset)
        response["Content-Disposition"] = 'attachment; filename="filtered_data.xlsx"'
        return response
    except Exception as exc:
        return HttpResponse(f"Unable to generate Excel file: {exc}", status=500)
