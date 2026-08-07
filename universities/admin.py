from django.contrib import admin

# Register your models here.
from .models import University, Program, AdmissionRequirement, LanguageRequirement


admin.site.register(University)
admin.site.register(Program)
admin.site.register(AdmissionRequirement)
admin.site.register(LanguageRequirement)