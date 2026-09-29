import django_filters
from django.db.models import Q
from universities.models import Program
from django.utils import timezone

STATUS_CHOICES = [
            ("OPENING_SOON", "Opening soon"),
            ("OPEN", "Open"),
            ("CLOSED", "Closed"),
        ]



class ProgramFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_search")
    city = django_filters.CharFilter(field_name="university__city", lookup_expr="icontains")
    degree = django_filters.CharFilter(field_name="degree", lookup_expr="iexact")
    teaching_language = django_filters.CharFilter(field_name="teaching_language", lookup_expr="iexact")
    application_platform = django_filters.CharFilter(field_name="application_platform", lookup_expr="iexact")
    nc_status = django_filters.CharFilter(field_name="nc_status", lookup_expr="iexact")
    semester = django_filters.CharFilter(field_name="semester", lookup_expr="iexact")
    vpd_required = django_filters.BooleanFilter(field_name="vpd_required")
    gre_required = django_filters.BooleanFilter(field_name="admission_requirement__gre")
    gmat_required = django_filters.BooleanFilter(field_name="admission_requirement__gmat")
    aps_required = django_filters.BooleanFilter(field_name="admission_requirement__aps_required")
    required_gpa = django_filters.NumberFilter(
        field_name="admission_requirement__required_german_gpa", lookup_expr="gte"
    )
    status = django_filters.ChoiceFilter(choices=STATUS_CHOICES, method="filter_status")
    ordering = django_filters.OrderingFilter(
        fields=(
            ("university__name", "name"),
            ("application_end", "deadline"),
            ("admission_requirement__required_german_gpa", "gpa"),
        )
    )

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) | Q(university__name__icontains=value)
        )

    def filter_status(self, queryset, name, value):
        today = timezone.localdate()
        if value == "OPENING_SOON":
            return queryset.filter(application_start__gt=today)
        if value == "OPEN":
            return queryset.filter(application_start__lte=today, application_end__gte=today)
        if value == "CLOSED":
            return queryset.filter(application_end__lt=today)
        return queryset

    class Meta:
        model = Program
        fields = ["search", "city", "degree", "teaching_language", "semester", "vpd_required",
                  "application_platform", "nc_status", "required_gpa", "aps_required",
                  "gmat_required", "gre_required", "status"]