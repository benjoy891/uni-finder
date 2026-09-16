import django_filters
from django.db.models import Q
from universities.models import University
from django.utils import timezone

STATUS_CHOICES = [
            ("OPENING_SOON", "Opening soon"),
            ("OPEN", "Open"),
            ("CLOSING_SOON", "Closing soon"),
            ("CLOSED", "Closed"),
        ]
CLOSING_SOON_THRESHOLD_DAYS = 14



class UniversityFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_search")
    city = django_filters.CharFilter(field_name="city", lookup_expr="icontains")
    degree = django_filters.CharFilter(field_name="programs__degree", lookup_expr="iexact")
    teaching_language  = django_filters.CharFilter(field_name="programs__teaching_language", lookup_expr="iexact")    
    application_platform   = django_filters.CharFilter(field_name="programs__application_platform", lookup_expr="iexact")
    nc_status  = django_filters.CharFilter(field_name="programs__nc_status", lookup_expr="iexact")
    semester  = django_filters.CharFilter(field_name="programs__semester", lookup_expr="iexact")
    gre_required = django_filters.BooleanFilter(field_name="programs__admission_requirement__gre")
    gmat_required = django_filters.BooleanFilter(field_name="programs__admission_requirement__gmat")
    aps_required = django_filters.BooleanFilter(field_name="programs__admission_requirement__aps_required")
    required_gpa = django_filters.NumberFilter(field_name="programs__admission_requirement__required_german_gpa", lookup_expr="gte")
    vpd_required = django_filters.BooleanFilter(field_name="programs__vpd_required")   
    status = django_filters.ChoiceFilter(choices=STATUS_CHOICES, method="filter_status")
    ordering = django_filters.OrderingFilter(
        fields=(
            ("name", "name"),
            ("programs__application_end", "deadline"),
            ("programs__admission_requirement__required_german_gpa", "gpa"),
        )
    )

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(programs__name__icontains=value)
        ).distinct()

    def filter_status(self, queryset, name, value):
        today = timezone.localdate()
        if value == "OPENING_SOON":
            return queryset.filter(
                programs__application_start__gt=today
            ).distinct()
        if value == "OPEN":
            return queryset.filter(
                programs__application_start__lte=today,
                programs__application_end__gte=today,
            ).distinct()
        if value == "CLOSED":
            return queryset.filter(
                programs__application_end__lt=today
            ).distinct()

        return queryset

    class Meta:
        model = University
        fields = ["search", "city", "degree", "teaching_language", "semester", "vpd_required",
                  "application_platform",  "nc_status", "required_gpa", "aps_required", "gmat_required", 
                  "gre_required", "status"]