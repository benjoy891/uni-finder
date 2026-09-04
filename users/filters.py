import django_filters
from django.db.models import Q
from universities.models import University
from django.utils import timezone



class UniversityFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(field_name="city", lookup_expr="iexact")
    degree = django_filters.CharFilter(field_name="programs__degree", lookup_expr="iexact")
    teaching_language  = django_filters.CharFilter(field_name="programs__teaching_language", lookup_expr="iexact")    
    application_platform   = django_filters.CharFilter(field_name="programs__application_platform", lookup_expr="iexact")
    nc_status  = django_filters.CharFilter(field_name="programs__nc_status", lookup_expr="iexact")
    semester  = django_filters.CharFilter(field_name="programs__semester", lookup_expr="iexact")
    application_start = django_filters.CharFilter(field_name="programs__application_start", lookup_expr="exact")
    application_end = django_filters.CharFilter(field_name="programs__application_end", lookup_expr="exact")

    search = django_filters.CharFilter(method="filter_search")
    open_applications = django_filters.CharFilter(method="filter_open_applications")

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(programs__name__icontains=value)
        ).distinct()

    def filter_open_applications(self, queryset, name, value):
        if value:
            today = timezone.localdate()
            return queryset.filter(
                programs__application_start__lte=today,
                programs__application_end__gte=today,
            ).distinct()
        return queryset

    class Meta:
        model = University
        fields = ["search", "open_applications", "country", "city", "degree", "teaching_language", "semester", "application_platform", 
                  "nc_status"]