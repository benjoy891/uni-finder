from rest_framework import serializers
from .models import University, AdmissionRequirement, LanguageRequirement, Program

class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ["id", "name", "country", "city", "address", "website", "created_at", "updated_at"]


class AdmissionRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdmissionRequirement
        fields = ["minimum_gpa", "minimum_german_gpa", "gre", "gmat", "aps_required", "notes"]


class LanuageRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = LanguageRequirement
        fields = ["language", "exam", "minimum_score"]

class ProgramSerializer(serializers.ModelSerializer):
    admission_requirement = AdmissionRequirementSerializer(read_only=True)
    language_requirements = LanuageRequirementSerializer(many=True, read_only=True)

    class Meta:
        model = Program
        fields = ["id", "name", "degree", "teaching_language", "semester", "application_start", "application_end",
                  "application_platform", "vpd_required", "nc_status", "program_url", "description", "admission_requirement",
                  "language_requirements"]



class UniversityDetailSerializer(serializers.ModelSerializer):
    programs = ProgramSerializer(many=True, read_only=True)
    class Meta:
        model = University
        fields = ["id", "name", "country", "city", "address", "website", "programs", "created_at", "updated_at"]
