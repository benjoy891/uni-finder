from rest_framework import serializers
from django.utils import timezone
from universities.models import Program
from .models import User
from django.contrib.auth import password_validation


class UserResgistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {
            "password": {"write_only": True, "required": True},
            "username": {"required": True},
            "email": {"required": True},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A user with this email already exists."
            )
        return value

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )


class StudentProgramListSerializer(serializers.ModelSerializer):
    university_id = serializers.IntegerField(source="university.id")
    name = serializers.CharField(source="university.name")
    country = serializers.CharField(source="university.country")
    city = serializers.CharField(source="university.city")
    address = serializers.CharField(source="university.address")
    website = serializers.URLField(source="university.website")
    program_name = serializers.CharField(source="name")
    status = serializers.SerializerMethodField()

    class Meta:
        model = Program
        fields = ["university_id", "name", "program_name", "country",
                  "city", "address", "website", "status"]

    def get_status(self, obj):
        today = timezone.localdate()
        if not obj.application_start or not obj.application_end:
            return "UNKNOWN"
        if obj.application_start > today:
            return "OPENING_SOON"
        if obj.application_start <= today <= obj.application_end:
            return "OPEN"
        return "CLOSED"