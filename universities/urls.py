from django.urls import path, include
from .views import UniversityListView, UniversityDetailView


urlpatterns = [
    path('', UniversityListView.as_view(), name="university-list"),
    path('<int:pk>/', UniversityDetailView.as_view(), name="university-detail"),
]