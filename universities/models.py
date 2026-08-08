from django.db import models

# Create your models here.
class University(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.TextField()
    website = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Universities"

    def __str__(self):
        return self.name


class Program(models.Model):
    DEGREE_CHOICES = [
        ("BACHELOR", "Bachelor"),
        ("MASTER", "Master"),
        ("PHD", "PhD"),
    ]
    LANGUAGE_CHOICES = [
        ("ENGLISH", "English"),
        ("GERMAN", "German"),
    ]
    SEMESTER_CHOICES = [
        ("WINTER", "Winter"),
        ("SUMMER", "Summer"),
    ]
    APPLICATION_PLATFORM_CHOICES = [
        ("DIRECT", "Direct"),
        ("UNI_ASSIST", "Uni-Assist"),
    ]
    NC_STATUS_CHOICES = [
        ("NC_FREE", "NC-Free"),
        ("NC", "NC"),
    ]

    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name="programs")
    name = models.CharField(max_length=255)
    degree = models.CharField(max_length=20, choices=DEGREE_CHOICES)
    teaching_language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES)
    semester = models.CharField(max_length=20, choices=SEMESTER_CHOICES)
    application_start = models.DateField(null=True, blank=True)
    application_end = models.DateField(null=True, blank=True)
    application_platform = models.CharField(max_length=20, choices=APPLICATION_PLATFORM_CHOICES)
    nc_status = models.CharField(max_length=10, choices=NC_STATUS_CHOICES)
    vpd_required = models.BooleanField(default=False)
    program_url = models.URLField(null=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.university.name})"


class AdmissionRequirement(models.Model):
    program = models.OneToOneField(Program, on_delete=models.CASCADE, related_name="admission_requirement")
    minimum_gpa = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    minimum_german_gpa = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    gre = models.BooleanField(default=False)
    gmat = models.BooleanField(default=False)
    aps_required = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"Requirements - {self.program.name}"




class LanguageRequirement(models.Model):
    LANGUAGE_CHOICES = [
        ("ENGLISH", "English"),
        ("GERMAN", "German"),
    ]
    EXAM_CHOICES = [
        ("IELTS", "IELTS"),
        ("TOEFL", "TOEFL"),
        ("TESTDAF", "TestDaF"),
        ("DSH", "DSH"),
        ("GOETHE", "Goethe"),
        ("TELC", "telc"),
    ]

    program = models.ForeignKey(Program,on_delete=models.CASCADE,related_name="language_requirements")
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES)
    exam = models.CharField(max_length=20, choices=EXAM_CHOICES)
    minimum_score = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.program.name} - {self.exam}"