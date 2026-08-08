from django.contrib import admin

# Register your models here.
from .models import University, Program, AdmissionRequirement, LanguageRequirement



@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "city",
        "website",
    )

    search_fields = (
        "name",
        "country",
        "city",
    )

    list_filter = (
        "country",
    )



class AdmissionRequirementInline(admin.StackedInline):
    model = AdmissionRequirement
    extra = 0


class LanguageRequirementInline(admin.TabularInline):
    model = LanguageRequirement
    extra = 0


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "university",
        "degree",
        "teaching_language",
        "semester",
        "nc_status",
    )

    search_fields = (
        "name",
        "university__name",
    )

    list_filter = (
        "degree",
        "teaching_language",
        "semester",
        "nc_status",
        "application_platform",
    )

    inlines = [
        AdmissionRequirementInline,
        LanguageRequirementInline,
    ]