from rest_framework import serializers
from django.db import transaction
from django.utils import timezone
from .models import University, AdmissionRequirement, LanguageRequirement, Program

class UniversitySerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    
    class Meta:
        model = University
        fields = ["id", "name", "country", "city", "address", "website", "status", "created_at", "updated_at"]

    def get_status(self, obj): 
        today = timezone.localdate()
        statuses = set()

        for program in obj.programs.all():
            if not program.application_start or not program.application_end:
                continue
            if program.application_start > today:
                statuses.add("OPENING_SOON")
            elif program.application_start <= today <= program.application_end:
                statuses.add("OPEN")
            elif program.application_end < today:
                statuses.add("CLOSED")

        if "OPEN" in statuses:
            return "OPEN"
        if "OPENING_SOON" in statuses:
            return "OPENING_SOON"
        if "CLOSED" in statuses:
            return "CLOSED"
        return "UNKNOWN"
    

class AdmissionRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdmissionRequirement
        fields = ["required_german_gpa", "gre", "gmat", "aps_required", "notes"]


class LanguageRequirementSerializer(serializers.ModelSerializer):
    required_score = serializers.SerializerMethodField()
    class Meta:
        model = LanguageRequirement
        fields = ["language", "exam", "required_score"]

    def get_required_score(self, obj):
        if obj.minimum_score_numeric is not None:
            return str(obj.minimum_score_numeric)
        if obj.minimum_level:
            return obj.minimum_level
        return None


class ProgramSerializer(serializers.ModelSerializer):
    admission_requirement = AdmissionRequirementSerializer(required=False)
    language_requirements = LanguageRequirementSerializer(many=True, required=False)

    class Meta:
        model = Program
        fields = ["id", "name", "degree", "teaching_language", "semester", "application_start", "application_end",
                  "application_platform", "vpd_required", "nc_status", "program_url", "description", "admission_requirement",
                  "language_requirements"]

    @transaction.atomic
    def create(self, validated_data):
        admission_data = validated_data.pop("admission_requirement", None)
        language_data = validated_data.pop("language_requirements", [])
        program = Program.objects.create(**validated_data)
        if admission_data:
            AdmissionRequirement.objects.create(
                program=program,
                **admission_data
            )
        for language_requirement in language_data:
            LanguageRequirement.objects.create(
                program=program,
                **language_requirement
            )
        return program

    @transaction.atomic
    def update(self, instance, validated_data):
        admission_data = validated_data.pop("admission_requirement", None)
        language_data = validated_data.pop("language_requirements", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if admission_data is not None:
            admission_requirement, created = (
                AdmissionRequirement.objects.get_or_create(
                    program=instance
                )
            )
            for attr, value in admission_data.items():
                setattr(admission_requirement, attr, value)
            admission_requirement.save()

        if language_data is not None:
            instance.language_requirements.all().delete()
            for language_requirement in language_data:
                LanguageRequirement.objects.create(
                    program=instance,
                    **language_requirement
                )
        return instance



class UniversityDetailSerializer(serializers.ModelSerializer):
    programs = ProgramSerializer(many=True, read_only=True)
    class Meta:
        model = University
        fields = ["id", "name", "country", "city", "address", "website", "programs", "created_at", "updated_at"]
